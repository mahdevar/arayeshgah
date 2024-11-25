FROM python:alpine
#FROM public.ecr.aws/docker/library/python:alpine
EXPOSE 8080
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
ENV PIP_NO_CACHE_DIR=off
COPY . .
RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt
RUN pip install gunicorn
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "--preload", "--threads=100", "--workers=9", "main:app"]
