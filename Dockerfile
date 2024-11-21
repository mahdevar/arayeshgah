#FROM python:alpine
FROM public.ecr.aws/docker/library/python:alpine
EXPOSE 8080
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONUTF8=1
#COPY requirements.txt requirements.txt
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN export CPUs=`expr $(nproc) \* 2 + 1000`
RUN echo $CPUs
#RUN python3 init.py
ENV P=$(( 2 * `nproc` + 1 ))
CMD gunicorn --preload --workers=$(( 2 * `nproc` + 1 )) --threads=100 --bind=0.0.0.0:8080 main:app
