import pytest


@pytest.mark.asyncio
async def test_format_vacancy_message_success(service):
    vacancy_data = {
        "name": "Python Developer",
        "url": "http://example.com",
        "employer": "Example Inc.",
        "workplaces": ["Remote"],
        "contract_types": ["Full-time"],
        "position_levels": ["Mid"],
        "category": "IT",
        "subcategory": "Development",
        "work_models": ["Remote"],
        "work_schedules": ["Flexible"],
        "subscribers": [123]
    }

    result = service._format_vacancy_message(vacancy_data)
    assert result == "formatted message"
    service.template.render.assert_called_once_with(**vacancy_data)

@pytest.mark.asyncio
async def test_send_vacancy_message_success(service, mock_bot):
    vacancy_data = {
        "name": "Python Developer",
        "url": "http://example.com",
        "employer": "Example Inc.",
        "workplaces": ["Remote"],
        "contract_types": ["Full-time"],
        "position_levels": ["Mid"],
        "category": "IT",
        "subcategory": "Development",
        "work_models": ["Remote"],
        "work_schedules": ["Flexible"],
        "subscribers": [123, 456]
    }

    await service.send_vacancy_message(vacancy_data)

    # Assert send_message called for each subscriber
    assert mock_bot.send_message.call_count == 2
    mock_bot.send_message.assert_any_call(
        chat_id=123,
        text="formatted message",
        parse_mode=pytest.importorskip("aiogram.enums").ParseMode.HTML
    )
    mock_bot.send_message.assert_any_call(
        chat_id=456,
        text="formatted message",
        parse_mode=pytest.importorskip("aiogram.enums").ParseMode.HTML
    )

@pytest.mark.asyncio
async def test_format_vacancy_message_missing_key(service):

    # no key "name" provided, should raise exception 
    vacancy_data = {
        "url": "http://example.com",
        "employer": "Example Inc.",
        "workplaces": ["Remote"],
        "contract_types": ["Full-time"],
        "position_levels": ["Mid"],
        "category": "IT",
        "subcategory": "Development",
        "work_models": ["Remote"],
        "work_schedules": ["Flexible"],
        "subscribers": [1,2,3]
    }

    service.template.render.side_effect = KeyError("name")

    with pytest.raises(KeyError):
        service._format_vacancy_message(vacancy_data)

def test_template_renders_correctly(real_template_service):
    vacancy_data = {
        "name": "Python Developer",
        "url": "https://example.com/job/1",
        "employer": "Tech Corp",
        "workplaces": ["Warsaw", "Remote"],
        "contract_types": ["Full-time", "B2B"],
        "position_levels": ["Mid", "Senior"],
        "category": "Software",
        "subcategory": "Backend",
        "work_models": ["Remote", "Hybrid"],
        "work_schedules": ["Flexible"],
        "subscribers": [1,2,3]
    }

    message = real_template_service._format_vacancy_message(vacancy_data)

    assert "Python Developer" in message
    assert "Tech Corp" in message
    assert "Warsaw" in message
    assert "Remote" in message
    assert "Full-time" in message
    assert "Backend" in message
    assert "Software" in message
    assert "Flexible" in message
    assert vacancy_data["url"] in message