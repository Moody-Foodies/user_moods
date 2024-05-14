FROM python:3.12-alpine

# Install system dependencies
RUN apk update && \
    apk add --no-cache bash

# Install Pipenv
RUN pip install --no-cache-dir pipenv

# Set working directory
WORKDIR /usr/src/app

# Copy Pipfiles
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system --deploy

# Copy application code
COPY user_mood ./user_mood
COPY bootstrap.sh ./

# Expose port
EXPOSE 5001

# Set entrypoint
ENTRYPOINT ["./bootstrap.sh"]
