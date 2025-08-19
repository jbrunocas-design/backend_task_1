## Description
This is a basic catalog system made with Django. The catalog contains products (sku, name, price, etc).

## Types of users who can access:
- Admins
  -  Can create, edit, delete products
  - Can delete other admins
- Anonymous
  - Can read products

## Actions available in the system
- WHEN Anonymous user visits website THEN System displays Main page, Main Page displays all products, Main page displays Log In option, Main page displays search bar
- WHEN Anonymous user queries valid product THEN System displays Product page, System logs metric
- WHEN Anonymous user queries invalid product THEN System displays error message
- WHEN Anonymous user logs in THEN admin page displayed, DB tables are displayed
- WHEN Admin Creates, Edits, deletes product THEN System notifies other admins (via console)

## Requirements
- Python
- pip install -r requirements.txt 
- Venv
- Clone this repo

## Run
```bash
python manage.py migrate # Generate local sqlite db
python manage.py createsuperuser # Create admin user
python manage.py runserver # run
```

