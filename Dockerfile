FROM python:3.7.0-alpine

ENV FILE csv_data.txt

COPY . /app/boardgames/
WORKDIR /app/boardgames/

RUN pip install pipenv &&\
    pipenv install pytest   
    
RUN pipenv run pytest -v

CMD pipenv run ./app-src/app.py ${FILE}
