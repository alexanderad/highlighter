FROM python:2-slim

ADD app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD app /app
ADD manage.py /

EXPOSE 8000
WORKDIR /
CMD python manage.py
