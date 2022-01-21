FROM python:3.9.6-alpine3.14

ARG PIP_ENV=production

WORKDIR /code

# Application user
RUN set -eux && \
    addgroup app && \
    adduser -h /code -G app -D app

# Prevents Python from writing *.pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install app requirements
COPY ./requirements /code/requirements/

RUN set -eux && \
    pip install -U pip && \
    pip install -r /code/requirements/${PIP_ENV}.txt

# Copy the application code
COPY . /code/

# Change the ownership of the application code
USER app:app

# Run the application
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
