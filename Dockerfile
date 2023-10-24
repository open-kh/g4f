FROM python:3.8-slim-buster

WORKDIR /

COPY /requirements.txt requirements.txt
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip

RUN pip install -r /requirements.txt
RUN pip install -r requirements.txt && pip install -r interference/requirements.txt

COPY . .

CMD [ "python", "-m" , "interference.app"]
