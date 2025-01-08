FROM python:3.11
WORKDIR /scrap_server

COPY . /scrap_server

RUN pip install requests

ENTRYPOINT ["python3", "buoygrab.py"]