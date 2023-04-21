FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

EXPOSE 5005

CMD sleep 5; rasa train; rasa run;