# Setup:
Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Servers:

Django:
python manage.py runserver

Celery Worker & Beat:
celery -A concert_ticketing worker --loglevel=info
celery -A concert_ticketing beat --loglevel=info

# Access Interfaces:
Admin Panel: http://localhost:8000/admin/ (manage events/tickets)
Frontend: http://localhost:8000/ (displays events)
API Endpoints: http://localhost:8000/api/events/, http://localhost:8000/api/tickets/
Google Sheets : https://docs.google.com/spreadsheets/d/1w4FrT6AHAVaJIuUi4Rc9MhdwsOCVrexXKUeKzwkgc7A/edit?usp=sharing (User input)
