# stockview_backend

A Django backend for stockview

## 1. Project setup
### 1.1 Requirements
- Add a .env file to stockview_backend/
- Add an entry for `ALPHAVANTAGE_API_KEY=<key_val>`
- You can get a key here: https://www.alphavantage.co/support/#api-key

### 1.2 Extra Steps
- If you want to run migrations you can run the following commands:
- `python manage.py makemigrations`
- `python manage.py migrate`
- Finally don't forget to create an admin with the command: `python manage.py createsuperuser`

### 1.3 Running the API
- API should work out of the box by simply running `docker-compose up`
- You can connect using `localhost:8000`