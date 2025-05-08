# Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip uninstall -y fiona
RUN pip install fiona
RUN pip uninstall -y geopandas
RUN pip install geopandas

COPY . .

CMD ["python", "app.py"]