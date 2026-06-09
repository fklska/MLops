FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir evidently pandas pyarrow
RUN mkdir -p /app/workspace
EXPOSE 9999
CMD ["evidently", "ui", "--path", "/app/workspace", "--port", "9999", "--host", "0.0.0.0"]