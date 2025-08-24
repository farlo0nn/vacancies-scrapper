import re 


from collections.abc import Callable
from typing import Any, Iterable
from scrapy.http import TextResponse
from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor
from pracujpl.services.selecting.pracujpl_vacancy_section_selector import PracujplVacancySectionSelector
from typing import Pattern

class PracujplLinkExtractor(LinkExtractor):

    def __init__(self, allow: str | Pattern[str] | Iterable[str | Pattern[str]] = ..., deny: str | Pattern[str] | Iterable[str | Pattern[str]] = ..., allow_domains: str | Iterable[str] = ..., deny_domains: str | Iterable[str] = ..., restrict_xpaths: str | Iterable[str] = ..., tags: str | Iterable[str] = ..., attrs: str | Iterable[str] = ..., canonicalize: bool = False, unique: bool = True, process_value: Callable[[Any], Any] | None = None, deny_extensions: str | Iterable[str] | None = None, restrict_css: str | Iterable[str] = ..., strip: bool = True, restrict_text: str | Pattern[str] | Iterable[str | Pattern[str]] | None = None):
        super().__init__(allow, deny, allow_domains, deny_domains, restrict_xpaths, tags, attrs, canonicalize, unique, process_value, deny_extensions, restrict_css, strip, restrict_text)
        self.vacancy_section_selector = PracujplVacancySectionSelector()

    def extract_links(self, response: TextResponse) -> list[Link]:
        vacancies_section = self.vacancy_section_selector.get_vacancy_section(response)
        links = super().extract_links(vacancies_section)
        return list(filter(lambda link: re.search(r'https?://(?:www\.)?pracuj\.pl/praca/[^,]+,oferta,\d+(?:\?[^\s]*)?', link.url), links))