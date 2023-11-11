runserver:
	python3 src/manage.py runserver

db:
	python3 src/manage.py makemigrations
	python3 src/manage.py migrate

setup:
	python3 -m pip install poetry
	poetry config virtualenvs.in-project true
	cp .env.example .env
	cd ./src/ && poetry install --no-root
