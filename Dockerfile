# Container image that runs your code
FROM python:3.11
WORKDIR /buoygrab

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY buoygrab.py /buoygrab

RUN pip install BeautifulSoup
RUN pip install requests
RUN pip install time

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["python", "/buoygrab/buoygrab.py"]
