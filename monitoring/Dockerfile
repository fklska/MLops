FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir evidently pandas pyarrow
RUN mkdir -p /app/workspace
EXPOSE 9090
CMD ["evidently", "ui", "--path", "/app/workspace", "--port", "9090", "--host", "0.0.0.0"]