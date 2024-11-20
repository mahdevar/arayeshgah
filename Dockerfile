#FROM python:alpine
FROM public.ecr.aws/docker/library/python:alpine
EXPOSE 8080
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
#COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN python3 init.py
CMD gunicorn --preload --workers=9 --threads=100 --bind=0.0.0.0:8080 main:app
