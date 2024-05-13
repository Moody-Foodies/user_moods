FROM python:3.12-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY user_moods ./user_moods

RUN pipenv install --system --deploy

EXPOSE 5001

ENTRYPOINT ["/usr/src/app/bootstrap.sh"]