# pull official base image
FROM python:3.11.6-bookworm
# set work directory
WORKDIR /usr/Vidify/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN apt-get update && apt-get install gcc g++ -y
RUN apt-get install ffmpeg -y
RUN apt-get install libpq-dev -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root




# copy project
COPY . .



# EXPOSE 8000

RUN chmod +x ./startup.sh

# CMD ["python3", "manage.py", "makemigrations", "&&", "python3", "manage.py", "migrate", "&&", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/usr/Vidify/src/startup.sh"]
