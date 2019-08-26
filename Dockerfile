FROM python:3.7-slim-buster

RUN groupadd -r flaskapp && useradd -r -g flaskapp -s /sbin/nologin flaskapp

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

RUN chown -R flaskapp:flaskapp /app
USER flaskapp

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]