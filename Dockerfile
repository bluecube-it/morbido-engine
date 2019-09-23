FROM python:3

WORKDIR /usr/src

RUN git clone http://gitlab.internal.bluecube.it/teo/morbido-api.git

WORKDIR /usr/src/morbido-api

RUN git checkout pre-release
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]
