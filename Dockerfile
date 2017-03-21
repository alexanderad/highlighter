FROM python:2.7-slim

ADD /app /src/app
ADD manage.py /src

RUN pip install -r /src/app/requirements.txt

EXPOSE 8000

WORKDIR /src
CMD python manage.py
