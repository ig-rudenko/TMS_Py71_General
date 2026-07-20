python manage.py migrate;
python manage.py test;
gunicorn django_project.wsgi:application -w 2 --bind 0.0.0.0:8000;