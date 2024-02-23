# Container image that runs your code
FROM python:3.11

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY buoygrab.py /buoygrab.py

RUN pip install BeautifulSoup
RUN pip install requests
RUN pip install time

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["python", "/buoygrab.py"]
