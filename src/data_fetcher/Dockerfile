FROM python:3.8-slim-buster
WORKDIR /data_fetcher
ADD . /data_fetcher
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "fetcher.py"]
