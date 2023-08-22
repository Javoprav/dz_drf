python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --input
coverage run --source='.' manage.py test
coverage html
deactivate