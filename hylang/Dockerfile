FROM python:3.9-slim-buster
WORKDIR /code

RUN apt-get update -y

RUN pip3 install pipenv
ADD Pipfile Pipfile.lock /code/
RUN pipenv install 

ADD . /code/
# RUN rm -r /usr/share/dict
ENTRYPOINT [ "pipenv", "run", "hy", "./boggle_solve.hy" ]