# Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt
RUN pip uninstall -y fiona
RUN pip install fiona
RUN pip uninstall -y geopandas
RUN pip install geopandas

COPY . .
# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]