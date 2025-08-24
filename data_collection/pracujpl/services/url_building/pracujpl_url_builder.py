import traceback


from pracujpl.interfaces.url_building import URLBuilder
from logger import logger 


class PracujplURLBuilder(URLBuilder):
    
    def __init__(self) -> None:
        super().__init__()

    def build_next_page_url(self, current_url) -> str:
        try:
            parsed = current_url.split("&pn=")
            logger.info(current_url)
            logger.info(parsed)

            next_page_url = \
                parsed[0] + \
                "&pn=" + \
                str(int(
                    parsed[1] if len(parsed) > 1 else 1  
                )
            +1)
            logger.info(f"NEXT PAGE URL is {next_page_url}")
            return next_page_url
        except Exception as e:
            logger.error(f"Failed to build url for next page. Traceback: {traceback.format_exc()}")
            raise e 