import traceback


from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models.vacancy_models import (
    Category, Subcategory
)
from models.telegram_models import (
    User, Location, ContractType, PositionLevel, WorkSchedule, WorkModel,
    user_location_association, user_contract_type_association,
    user_position_level_association, user_work_schedule_association,
    user_work_model_association, user_category_association,
    user_subcategory_association
)
from models.config import SessionLocal
from logger import logger 

class UserRepository:

    def upsert_user_from_dict(self, data: dict):
        with SessionLocal() as session: 
            user_id = data["id"]
            username = data.get("username")
            preferences = data.get("preferences", {})

            user = session.get(User, user_id)
            if not user:
                user = User(id=user_id, username=username)
                session.add(user)
            else:
                user.username = username 

            def sync_association(assoc_table, model_cls, preference_key):
                if preference_key not in preferences:
                    session.execute(
                        assoc_table.delete().where(assoc_table.c.user_id == user.id)
                    )
                    return

                current = {
                    row[0] for row in
                    session.execute(
                        assoc_table.select().with_only_columns(assoc_table.c[f"{model_cls.__tablename__}_id"])
                        .where(assoc_table.c.user_id == user.id)
                    )
                }

                selected_values = set(preferences[preference_key])

                objs = []
                for value in selected_values:
                    obj = session.query(model_cls).filter_by(name=value).first()
                    if not obj:
                        obj = model_cls(name=value)
                        session.add(obj)
                        session.flush()  
                    objs.append(obj)

                selected_ids = {o.id for o in objs}

                to_delete = current - selected_ids
                if to_delete:
                    session.execute(
                        assoc_table.delete().where(
                            (assoc_table.c.user_id == user.id) &
                            (assoc_table.c[f"{model_cls.__tablename__}_id"].in_(to_delete))
                        )
                    )

                to_add = selected_ids - current
                if to_add:
                    session.execute(
                        assoc_table.insert(),
                        [{"user_id": user.id, f"{model_cls.__tablename__}_id": i} for i in to_add]
                    )

            sync_association(user_location_association, Location, "location")
            sync_association(user_category_association, Category, "category")
            sync_association(user_subcategory_association, Subcategory, "subcategory")
            sync_association(user_contract_type_association, ContractType, "contract_type")
            sync_association(user_position_level_association, PositionLevel, "experience")
            sync_association(user_work_schedule_association, WorkSchedule, "work_schedule")
            sync_association(user_work_model_association, WorkModel, "work_model")

            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise


    def get_user_data(self, data: dict) -> dict:
        with SessionLocal() as session: 
            user_id = data["user_id"]

            user = session.get(User, user_id)
            if not user:
                return {}

            preferences = {}
            def collect_association(assoc_table, model_cls, preference_key):
                rows = session.execute(
                    assoc_table.select()
                    .with_only_columns(assoc_table.c[f"{model_cls.__tablename__}_id"])
                    .where(assoc_table.c.user_id == user.id)
                ).fetchall()

                if not rows:
                    preferences[preference_key] = []
                    return

                ids = [r[0] for r in rows]
                objs = session.query(model_cls).filter(model_cls.id.in_(ids)).all()
                preferences[preference_key] = [o.name for o in objs]

            collect_association(user_location_association, Location, "location")
            collect_association(user_category_association, Category, "category")
            collect_association(user_subcategory_association, Subcategory, "subcategory")
            collect_association(user_contract_type_association, ContractType, "contract_type")
            collect_association(user_position_level_association, PositionLevel, "experience")
            collect_association(user_work_schedule_association, WorkSchedule, "work_schedule")
            collect_association(user_work_model_association, WorkModel, "work_model")

            return preferences

            
    def is_user_consuming(self, user_id: int, change_value: bool = False): 
        with SessionLocal() as session: 
            try:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    return False

                if change_value:
                    user.is_consuming = not user.is_consuming
                    session.commit()

                return user.is_consuming
            except SQLAlchemyError as e:
                session.rollback()
                logger.exception(f"DB error while processing consuming flag for user {user_id}")
                raise
