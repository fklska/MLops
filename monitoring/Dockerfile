FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir evidently pandas pyarrow
RUN mkdir -p /app/workspace

EXPOSE 9999
ENV EVIDENTLY_WORKSPACE=/app/workspace

CMD ["evidently", "ui", "--port", "9999", "--host", "0.0.0.0"]