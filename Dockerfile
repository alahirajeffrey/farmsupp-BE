FROM python:3.9-slim

WORKDIR /farmsup

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY .  .

CMD ["bash", "run_dev_server.sh"]
