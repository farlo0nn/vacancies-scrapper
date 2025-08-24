import pytest 
from unittest.mock import AsyncMock, Mock, patch
from services.notifications import NotificationsService
from services.notifications.utils import load_html_template

@pytest.fixture
def mock_bot():
    bot = AsyncMock()
    return bot

@pytest.fixture
def service(mock_bot):
    with patch("services.notifications.notifications_service.load_html_template") as mock_template_loader:
        mock_template = Mock()
        mock_template.render.return_value = "formatted message"
        mock_template_loader.return_value = mock_template
        service = NotificationsService(mock_bot)
        yield service


@pytest.fixture
def real_template_service():
    service = NotificationsService(bot=None) 
    service.template = load_html_template() 
    return service