from dataclasses import dataclass


@dataclass
class Vacancy:
    workplace: str = ""
    contract_types: str = "" 
    work_schedules: str = ""
    position_levels: str = ""
    work_models: str = ""
    optional_cv: bool = False 

    def __repr__(self) -> str:
        return f"workplace: {self.workplace}, contract types: {self.contract_types}"