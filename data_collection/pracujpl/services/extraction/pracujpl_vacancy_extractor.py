from scrapy.http import TextResponse
from pracujpl.interfaces import VacancyExtractor
from pracujpl.interfaces.data_models import VacancyData
from pracujpl.services.selecting.pracujpl_criterion_selector import PracujplCriterionSelector


class PracujplVacancyExtractor(VacancyExtractor):

    def __init__(self) -> None:
        self.criterion_selector = PracujplCriterionSelector()
        super().__init__()

    def extract_vacancy_data(self, response: TextResponse) -> VacancyData:
        
        vacancy_id = response.meta["vacancy_id"]
        vacancy_url = response.meta["vacancy_url"]

        name = self.criterion_selector.get_criterion_data(response, "name")
        category, subcategory = self.criterion_selector.get_criterion_data(response, "category")
        
        vacancy = VacancyData(
            id=int(vacancy_id),
            url=vacancy_url,
            name=name, 
            employer=self.criterion_selector.get_criterion_data(response, "employer"),
            workplaces=self.criterion_selector.get_criterion_data(response, "workplaces"),
            contract_types=self.criterion_selector.get_criterion_data(response, "contract-types"),
            work_schedules=self.criterion_selector.get_criterion_data(response, "work-schedules"),
            position_levels=self.criterion_selector.get_criterion_data(response, "position-levels"),
            work_models=self.criterion_selector.get_criterion_data(response, "work-modes"),
            optional_cv=self.criterion_selector.get_criterion_data(response, "optional-cv"),
            salary=self.criterion_selector.get_criterion_data(response, "salary") or "",
            category=category or "",
            subcategory=subcategory or ""
        )

        return vacancy