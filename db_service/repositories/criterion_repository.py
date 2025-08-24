from typing import List 
from models import SessionLocal
from models.telegram_models import Location, WorkModel, WorkSchedule, PositionLevel, ContractType
from models.vacancy_models import Category
from sqlalchemy.exc import SQLAlchemyError
from exceptions import InvalidCategory
from logger import logger

class CriterionRepository:

    def get_criterion_values(self, criterion: str) -> List[str]:
        try:
            model = None 
            match criterion:
                case "location":
                    model = Location
                case "work_schedule":
                    model = WorkSchedule
                case "work_model":
                    model = WorkModel
                case "experience":
                    model = PositionLevel
                case "category":
                    model = Category
                case "contract_type":
                    model = ContractType
                case _:
                    raise InvalidCategory
            session = SessionLocal()
            response = session.query(model).all()
            values = [row.name for row in response]
            return values
        except InvalidCategory:
            logger.error(f"Invalid criterion was specified during values lookup. Criterion name: {criterion}")
            return []
        except SQLAlchemyError:
            logger.exception(f"Failed to get {criterion} values")
            raise