FROM python:3.10-slim

# Set environment vars
ENV AIRFLOW_HOME=/opt/airflow

# Install dependencies
COPY requirements.txt .
# COPY .env /opt/airflow/.env

RUN pip install --no-cache-dir streamlit
RUN pip install --no-cache-dir apache-airflow[sqlite]==2.7.2 \
    && pip install --no-cache-dir -r requirements.txt

# Create expected folders
RUN mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins /opt/airflow/scripts

# Set working directory
WORKDIR /opt/airflow

# Copy source code
COPY . .

# Default command (overridden by compose)
CMD ["airflow", "webserver"]
