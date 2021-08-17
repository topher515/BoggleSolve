FROM python:2.7-slim-buster
WORKDIR /code

RUN apt-get update -y

ADD . /code/
# RUN rm -r /usr/share/dict
ENTRYPOINT [ "python", "./boggle.py" ]