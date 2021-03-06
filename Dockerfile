FROM python:3.8-slim
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY api /api
COPY models /models
COPY orm /orm
CMD  uvicorn api.main:app --host "0.0.0.0" --port 8080