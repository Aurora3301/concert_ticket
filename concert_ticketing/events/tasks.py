from celery import shared_task
import logging

from events.google_sheets import GoogleSheetSync

logger = logging.getLogger(__name__)
@shared_task
def sync_google_sheets_task():
    syncer = GoogleSheetSync()
    success, message, synced_data = syncer.sync_to_cms()
    
    # Detailed logging
    for event in synced_data:
        logger.info(
            f"Synced event: {event['event_name']}\n"
            f"Date: {event['date']}\n"
            f"Venue: {event['venue']}\n"
            f"Description: {event['description']}\n"
            f"Ticket: {event['ticket_type']} "
            f"(Price: ${event['price']}, Qty: {event['quantity']})\n"
            "-------------------------"
        )
        
    return {
        "success": success,
        "message": message,
        "data": synced_data
    }