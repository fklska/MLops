FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir pandas evidently datasets
COPY drift_service.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]