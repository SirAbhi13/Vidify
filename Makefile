runserver:
	python3 src/manage.py runserver

db:
	python3 src/manage.py makemigrations
	python3 src/manage.py migrate
