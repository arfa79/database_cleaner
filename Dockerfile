FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /backup

# Copy the supervisor configuration file into the container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy the current directory contents into the container
COPY . .

# Define the command to run supervisor
CMD ["/usr/bin/supervisord"]
