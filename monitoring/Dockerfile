FROM python:3.10-slim
WORKDIR /app

RUN pip install --no-cache-dir evidently pandas pyarrow fastapi uvicorn
RUN mkdir -p /app/workspace

COPY init_project.py /app/

EXPOSE 9999

ENV EVIDENTLY_WORKSPACE=/app/workspace
ENV EVIDENTLY_HOST=0.0.0.0
ENV EVIDENTLY_PORT=9999

CMD ["sh", "-c", "python init_project.py && evidently ui --host 0.0.0.0 --port 9999"]