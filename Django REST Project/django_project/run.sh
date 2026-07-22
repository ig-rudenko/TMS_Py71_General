python manage.py migrate;
gunicorn django_project.wsgi:application -w 2 --bind 0.0.0.0:8000;