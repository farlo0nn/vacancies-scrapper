import traceback


from models import SessionLocal
from models.vacancy_models import Vacancy, Employer, Category, Subcategory
from logger import logger 
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text 
from typing import List 

class VacancyRepository:

    def __init__(self) -> None:        
        self.employer_cache = {}
        self.category_cache = {}
        self.subcategory_cache = {}


    def exists(self, vacancy_id: int) -> bool:
        with SessionLocal() as session: 
            return session.query(Vacancy).filter_by(id=vacancy_id).first() is not None 
        
    def create(self, vacancy_json: int) -> int: 
        with SessionLocal() as session: 
            try:

                employer_id = self._get_or_create_employer(session, vacancy_json["employer"])
                category_id = self._get_or_create_category(session, vacancy_json["category"])
                subcategory_id = self._get_or_create_subcategory(session, vacancy_json["subcategory"], category_id)
            
                vacancy = Vacancy(
                    id=vacancy_json["id"],
                    url=vacancy_json["url"],
                    name=vacancy_json["name"],
                    salary=vacancy_json.get("salary"),
                    employer_id=employer_id,
                    subcategory_id=subcategory_id,
                    contract_types=vacancy_json.get("contract_types"),
                    workplaces=vacancy_json.get("workplaces"),
                    work_schedules=vacancy_json.get("work_schedules"),
                    position_levels=vacancy_json.get("position_levels"),
                    work_models=vacancy_json.get("work_models"),
                    optional_cv=vacancy_json.get("optional_cv", False)
                )
            
                session.add(vacancy)
                session.commit()
                logger.info(f"Vacancy {vacancy_json["id"]} saved to database successfully")
            except Exception as e:
                logger.info(f"Failed to save vacancy: {vacancy_json["id"]} to db")
                session.rollback()
        

    
    def _get_or_create_employer(self, session, employer_name):
        if employer_name in self.employer_cache:
            return self.employer_cache[employer_name]
        
        try:
            employer = session.query(Employer).filter_by(name=employer_name).first()
            if employer:
                self.employer_cache[employer_name] = employer.id
                return employer.id
            
            try:
                employer = Employer(name=employer_name)
                session.add(employer)
                session.flush() 
                self.employer_cache[employer_name] = employer.id
                return employer.id
            except IntegrityError:
                session.rollback()
                employer = session.query(Employer).filter_by(name=employer_name).first()
                if employer:
                    self.employer_cache[employer_name] = employer.id
                    return employer.id
                else:
                    raise Exception(f"Could not create or find employer: {employer_name}")
                    
        except Exception as e:
            logger.error(f"Error handling employer {employer_name}: {str(e)}")
            raise

    def _get_or_create_category(self, session, category_name):
        if category_name in self.category_cache:
            return self.category_cache[category_name]
        
        try:
            category = session.query(Category).filter_by(name=category_name).first()
            if category:
                self.category_cache[category_name] = category.id
                return category.id
            
            try:
                category = Category(name=category_name)
                session.add(category)
                session.flush()
                self.category_cache[category_name] = category.id
                return category.id
            except IntegrityError:
                session.rollback()
                category = session.query(Category).filter_by(name=category_name).first()
                if category:
                    self.category_cache[category_name] = category.id
                    return category.id
                else:
                    raise Exception(f"Could not create or find category: {category_name}")
                    
        except Exception as e:
            logger.error(f"Error handling category {category_name}: {str(e)}")
            raise

    def _get_or_create_subcategory(self, session, subcategory_name, category_id):
        if subcategory_name in self.subcategory_cache:
            return self.subcategory_cache[subcategory_name]
        
        try:
            subcategory = session.query(Subcategory).filter_by(name=subcategory_name).first()
            if subcategory:
                self.subcategory_cache[subcategory_name] = subcategory.id
                return subcategory.id
            
            try:
                subcategory = Subcategory(name=subcategory_name, category_id=category_id)
                session.add(subcategory)
                session.flush()
                self.subcategory_cache[subcategory_name] = subcategory.id
                return subcategory.id
            except IntegrityError:
                session.rollback()
                subcategory = session.query(Subcategory).filter_by(name=subcategory_name).first()
                if subcategory:
                    self.subcategory_cache[subcategory_name] = subcategory.id
                    return subcategory.id
                else:
                    raise Exception(f"Could not create or find subcategory: {subcategory_name}")
                    
        except Exception as e:
            logger.error(f"Error handling subcategory {subcategory_name}: {str(e)}")
            raise

        
    def determine_target_users(self, vacancy_id) -> List[int]: 
        with SessionLocal() as session: 
            try: 
                response = session.execute(text(
                f"""
                with v_data as (
                    select v.id as id, c.id as category_id, c.name as category, s.name as subcategory, v.contract_types, v.position_levels, v.workplaces, v.work_models, v.work_schedules
                    from vacancies v
                    join subcategory s on v.subcategory_id = s.id
                    join category c on s.category_id = c.id
                    where v.id = {vacancy_id}
                )
                
                select distinct u.id
                from "user" u
                cross join v_data vd
                where
                    u.is_consuming and
                    (not exists(select 1 from users_category_association where user_id = u.id)
                    or (not exists(select 1 from users_subcategory_association usa
                            join subcategory sc on usa.subcategory_id = sc.id
                            where usa.user_id = u.id and sc.category_id = vd.category_id)
                        and exists(select 1 from users_category_association uca
                            join category c on uca.category_id = c.id
                            where uca.user_id = u.id and c.name = vd.category)))
                    and (not exists(select 1 from users_subcategory_association where user_id = u.id)
                    or exists(select 1 from users_subcategory_association usa2
                                        join subcategory s on usa2.subcategory_id = s.id
                                        where usa2.user_id = u.id and vd.subcategory = s.name))
                    and (not exists(select 1 from users_position_level_association where user_id = u.id)
                    or exists(select 1 from users_position_level_association upla
                                        join position_level p on upla.position_level_id = p.id
                                        where upla.user_id = u.id and vd.position_levels @> to_jsonb(p.name)))
                    and (not exists(select 1 from users_location_association where user_id = u.id)
                    or exists(select 1 from users_location_association ula
                                        join location l on ula.location_id = l.id
                                        where ula.user_id = u.id and vd.workplaces @> to_jsonb(l.name)))
                    and (not exists(select 1 from users_contract_types_association where user_id = u.id)
                    or exists(select 1 from users_contract_types_association ucta
                                        join contract_type ct on ucta.contract_type_id = ct.id
                                        where ucta.user_id = u.id and vd.contract_types @> to_jsonb(ct.name)))
                    and (not exists(select 1 from users_work_schedule_association where user_id = u.id)
                    or exists(select 1 from users_work_schedule_association uwsa
                                        join work_schedule ws on uwsa.work_schedule_id = ws.id
                                        where uwsa.user_id = u.id and vd.work_schedules @> to_jsonb(ws.name)))
                    and (not exists(select 1 from users_work_model_association where user_id = u.id)
                    or exists(select 1 from users_work_model_association uwma
                                        join work_model wm on uwma.work_model_id = wm.id
                                        where uwma.user_id = u.id and vd.work_models @> to_jsonb(wm.name)));
                """))

                target_users = [row[0] for row in response.fetchall()]
                logger.info(target_users)
                return target_users
            except Exception as e:
                logger.error(f"Failed to get target users for vacancy: {vacancy_id}. Traceback: {traceback.format_exc()}")