FROM python:alpine
#FROM public.ecr.aws/docker/library/python:alpine
WORKDIR /app
COPY requirements.txt /
ENV PIP_NO_CACHE_DIR=off
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
RUN apk add curl
RUN pip install --upgrade pip
RUN pip install --requirement /requirements.txt
RUN pip install gunicorn
EXPOSE 8000
CMD python initialize.py && gunicorn --bind=:8000 --reload --threads=100 --workers=$(($(nproc) * 2 + 1)) main:app
