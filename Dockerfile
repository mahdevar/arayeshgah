FROM python:alpine
#FROM public.ecr.aws/docker/library/python:alpine
WORKDIR /app
ENV PIP_NO_CACHE_DIR=off
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
COPY requirements.txt requirements.txt
RUN apk add curl
RUN pip install --upgrade pip
RUN pip install --requirement requirements.txt
RUN pip install gunicorn
EXPOSE 8000
CMD ["gunicorn", "--preload", "--reload", "--threads=100", "--workers=3", "main:app"]
