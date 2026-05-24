FROM python:3.12-slim
WORKDIR /app
COPY . .
EXPOSE 8080
RUN pip install --no-cache-dir torch==2.11.0+cpu torchvision==0.26.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
CMD ["celery", "-A", "main", "worker", "--loglevel=info", "--pool=solo"]