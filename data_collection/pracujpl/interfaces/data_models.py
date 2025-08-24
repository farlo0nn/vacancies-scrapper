import json


from dataclasses import dataclass, asdict
from typing import List 
from logger import logger 


@dataclass
class VacancyData:
    id: int
    url: str 
    name: str 
    employer: str 
    workplaces: List[str]
    contract_types: List[str]
    work_schedules: List[str]
    position_levels: List[str]
    work_models: List[str]
    optional_cv: bool 
    salary: str 
    category: str 
    subcategory: str 

    def asDict(self):
        return asdict(self)
    