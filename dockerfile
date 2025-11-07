
FROM python:3.10-slim


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./apps /code/apps


CMD ["fastapi", "run", "apps/main.py", "--port", "80"]


