FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir evidently pandas pyarrow
RUN mkdir -p /app/workspace

EXPOSE 9999

ENV EVIDENTLY_WORKSPACE=/app/workspace
ENV EVIDENTLY_HOST=0.0.0.0
ENV EVIDENTLY_PORT=9999

CMD ["evidently", "ui"]