FROM python:alpine
#FROM public.ecr.aws/docker/library/python:alpine
EXPOSE 5000
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
COPY --link . .
RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt
RUN pip install gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--threads=100", "--workers=9", "main:app"]
