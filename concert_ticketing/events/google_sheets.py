import gspread
from google.oauth2.service_account import Credentials  # <-- CHANGE THIS
from django.conf import settings
from django.utils import timezone
from .models import Event, Ticket
import logging
import os
import gspread

logger = logging.getLogger(__name__)

class GoogleSheetSync:
    def __init__(self):
        self.creds_path = os.path.join(settings.BASE_DIR, 'credentials.json')
        self.spreadsheet_url = settings.GOOGLE_SHEET_URL
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

    def _get_client(self): 
        """Modern Google Auth"""
        creds = Credentials.from_service_account_file(
            self.creds_path,
            scopes=self.scopes
        )
        return gspread.authorize(creds)
    
    def sync_to_cms(self):
        synced_data = []
        try:
            client = self._get_client()
            sheet = client.open_by_url(self.spreadsheet_url).worksheet("Sheet1")
            records = sheet.get_all_records()

            for idx, row in enumerate(records, start=2):
                try:
                    # Parse date with timezone support
                    event_date = timezone.make_aware(
                        timezone.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M')
                    )

                    # Track ALL data from sheet
                    event_data = {
                        'event_name': row['Event Name'],
                        'date': row['Date'],
                        'venue': row['Venue'],
                        'description': row['Description'],
                        'ticket_type': row['Ticket Type'],
                        'price': row['Price'],
                        'quantity': row['Quantity']
                    }
                    synced_data.append(event_data)

                    # Event sync
                    event, created = Event.objects.update_or_create(
                        name=row['Event Name'],
                        defaults={
                            'date': event_date,
                            'venue': row['Venue'],
                            'description': row['Description']
                        }
                    )

                    # Ticket sync
                    Ticket.objects.update_or_create(
                        event=event,
                        ticket_type=row['Ticket Type'],
                        defaults={
                            'price': row['Price'],
                            'quantity_available': row['Quantity']
                        }
                    )

                except KeyError as e:
                    logger.error(f"Missing column in row {idx}: {str(e)}")
                except Exception as e:
                    logger.error(f"Error processing row {idx}: {str(e)}")

            return True, f"Synced {len(synced_data)} events successfully", synced_data

        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            return False, str(e), []

    def sync_to_sheet(self):
        """Sync from CMS to Google Sheets (for admin updates)"""
        try:
            client = self._get_client()
            sheet = client.open_by_url(self.spreadsheet_url).worksheet("Main Data")
            
            # Clear existing data (except header)
            if sheet.row_count > 1:
                sheet.delete_rows(2, sheet.row_count)
            
            # Get all events with related tickets
            events = Event.objects.prefetch_related('tickets').all()
            
            # Prepare data
            data = []
            for event in events:
                for ticket in event.tickets.all():
                    data.append([
                        event.name,
                        event.date.strftime('%Y-%m-%d %H:%M'),
                        event.venue,
                        event.description,
                        ticket.ticket_type,
                        str(ticket.price),
                        str(ticket.quantity_available)
                    ])
            
            # Batch update
            if data:
                sheet.append_rows(data)
            
            return True, f"Updated sheet with {len(data)} entries"

        except Exception as e:
            logger.error(f"Sheet update failed: {str(e)}")
            return False, str(e)