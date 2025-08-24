from jinja2 import Template, Environment, FileSystemLoader, select_autoescape
from config import TEMPLATE_DIR, VACANCY_MESSAGE_TEMPLATE_FILE

def load_html_template() -> Template:
    env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            autoescape=select_autoescape(["html", "xml"])
        )

    template = env.get_template(VACANCY_MESSAGE_TEMPLATE_FILE)
    return template 
