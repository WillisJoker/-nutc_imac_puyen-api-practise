FROM python:3.8.7

RUN mkdir /puyen-test

WORKDIR /puyen-test

COPY * .

RUN pip freeze > requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
