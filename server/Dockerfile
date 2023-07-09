FROM python:3.11.4-slim-bullseye

WORKDIR /src/app

# RUN apt update

# RUN apt install postgresql -y

RUN python3 -m venv venv

RUN . venv/bin/activate

COPY . .

RUN find . -type d -name __pycache__ -exec rm -r {} \+

RUN pip3 install -r requirements.txt

CMD ["python3", "server.py"]