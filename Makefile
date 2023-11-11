runserver:
	python3 src/manage.py runserver

db:
	python3 src/manage.py makemigrations
	python3 src/manage.py migrate

setup:
	python3 -m pip install poetry
	poetry config virtualenvs.in-project true
	cd src/
	poetry install --no-root
	cp .env.example .env
