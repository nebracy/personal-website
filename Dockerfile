FROM python:3.7-slim-buster

WORKDIR /app

COPY . ./
RUN pip install -r requirements.txt

RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]