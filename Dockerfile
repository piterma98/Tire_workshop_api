FROM python:3.9-slim-buster
WORKDIR /backend
ADD ./docker-scripts.sh /backend/docker-scripts.sh
RUN chmod +x /backend/docker-scripts.sh && /backend/docker-scripts.sh
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
COPY requirements_docker.txt .
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements_docker.txt
ADD . /backend
RUN mkdir -p /backend/static
RUN python manage.py collectstatic --noinput --clear
