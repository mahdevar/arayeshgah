FROM python:alpine
#FROM public.ecr.aws/docker/library/python:alpine
EXPOSE 8080
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install --requirement requirements.txt
RUN pip3 install gunicorn
ENTRYPOINT ["gunicorn", "--preload", "--workers=9", "--threads=100", "--bind=0.0.0.0:8080", "main:app"]
