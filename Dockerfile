FROM python:3.8-slim
COPY api /api
COPY requirements.txt /
RUN pip install -r requirements.txt
CMD  uvicorn api.main:app --host "0.0.0.0" --port 8080