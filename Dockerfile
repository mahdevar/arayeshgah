#FROM python:alpine
FROM public.ecr.aws/docker/library/python:alpine
EXPOSE 8000
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
#COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
CMD ["gunicorn", "--preload" , "--workers=9", "--threads=100", "--bind=0.0.0.0:8000", "main:app"]
