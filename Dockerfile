FROM public.ecr.aws/starcat/python:latest

WORKDIR /app

COPY . ./
RUN pip install -r requirements.txt \
    gunicorn

RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]