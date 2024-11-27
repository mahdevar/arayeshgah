FROM python:alpine
#FROM public.ecr.aws/docker/library/python:alpine
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
#COPY --link . .
COPY . .
RUN apk add curl
RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt
RUN pip install gunicorn
EXPOSE 5000
CMD ["gunicorn", "--bind=:5000", "--preload", "--threads=100", "--workers=9", "main:app"]
