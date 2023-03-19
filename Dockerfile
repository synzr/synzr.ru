FROM python:3.11

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade gunicorn

COPY . /usr/src/app/

CMD ["gunicorn", "--conf", "configs/gunicorn.py", "--bind", "0.0.0.0:80", "app:app"]
