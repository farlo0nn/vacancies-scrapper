import re 


from typing import Tuple, List 
from scrapy.http import TextResponse
from pracujpl.interfaces.selecting import CriterionSelector


class PracujplCriterionSelector(CriterionSelector):

    def __init__(self) -> None:
        super().__init__()

    def get_criterion_data(self, response: TextResponse, feature: str) -> str|Tuple[str]|List[str]|bool:
        match feature:
            case "salary":
                return self._get_salary_data(response)
            case "name":
                return self._get_name_data(response)
            case "employer":
                return self._get_employer_data(response)
            case "category":
                return self._get_category_lines(response)
            case "optional-cv":
                return self._get_optional_cv(response)
            case _:
                texts = response.xpath(f'//li[@data-scroll-id="{feature}"]//text()').getall()
                return [val.strip() for text in texts for val in text.split(',') if val.strip()]


    def _get_category_lines(self, response) -> Tuple[str]:
        category_lines = response.xpath(
            '//text()[normalize-space()="Praca"]/following::text()'
        ).getall()
        
        if category_lines is None:
            return None 
        
        clean_lines = [line.strip() for line in category_lines if line.strip()]
        
        category = clean_lines[1] if len(clean_lines) > 1 else None 
        subcategory = clean_lines[2] if len(clean_lines) > 2 else None 

        return (category, subcategory)

    def _get_salary_data(self, response: TextResponse) -> str | None:
        salary_data = response.xpath('//div[@data-test="text-earningAmount"]//text()').get()
        if not salary_data:
            return None
        salary_data = ''.join(re.findall(r'[^\s]', salary_data))
        return salary_data

    def _get_name_data(self, response: TextResponse) -> str:
        return response.xpath('//h1[@data-test="text-positionName"]//text()').get()

    def _get_employer_data(self, response: TextResponse) -> str:
        return response.xpath('//h2[@data-test="text-employerName"]//text()').get()
    
    def _get_optional_cv(self, response: TextResponse) -> bool:
        optional_cv = response.xpath('//li[@data-scroll-id="{feature}"]//text()').get()
        return optional_cv is not None 