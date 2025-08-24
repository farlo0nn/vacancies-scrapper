import traceback


from services.kafka.client import kafka_client
from services.notifications import notifications_service
from logger import logger 


@kafka_client.on_message_handler("telegram_vacancy")
async def send_vacancy(data: dict, topic: str):
    logger.info(f"Received new vacancy on {topic} topic")
    try:
        await notifications_service.send_vacancy_message(data)
        logger.info(f"Vacancy was successfully sent to its subscribers")
    except Exception as e:
        logger.error(f"Error occurred while sending vacancy {data['id']} to its subscribers \nTraceback: {traceback.format_exc()}")
        raise e 
    
@kafka_client.on_message_handler(["criterion_response", "is_user_consuming_response", "get_user_data_response"])
async def listen_responses(data: dict, topic: str):
        request_id = data.get("request_id")
        if request_id is None: 
            logger.error("No request id in criterion response")
            return
        logger.info("Criterion Response was received")
        fut = kafka_client.pending_requests.pop(request_id, None)
        if fut and not fut.done():
            fut.set_result(data)
        else:
            logger.warning(f"No pending request found for request_id={request_id}")