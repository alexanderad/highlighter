FROM python:2

# install mercury-parser
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt update && apt install -y yarn && \
    yarn global add @postlight/mercury-parser

ADD app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD app /app
ADD manage.py /

EXPOSE 8000
WORKDIR /
CMD python manage.py
