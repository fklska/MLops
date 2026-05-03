FROM python:3.12-alpine
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]