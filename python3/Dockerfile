FROM python:3.9-slim-buster
WORKDIR /app

RUN apt-get update -y

RUN pip3 install pipenv
ADD Pipfile Pipfile.lock /app/
RUN pipenv install 

ADD . /app/
# RUN rm -r /usr/share/dict
ENTRYPOINT [ "pipenv", "run", "./boggle_solve.py" ]