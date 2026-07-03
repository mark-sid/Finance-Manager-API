FROM python:3.12-slim AS builder
 
RUN mkdir /app
 
WORKDIR /app
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
RUN pip install --upgrade pip 
 
COPY requirements.txt /app/
 
RUN pip install --no-cache-dir -r requirements.txt
 
# Stage 2
FROM python:3.12-slim
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
WORKDIR /app
 
COPY --chown=appuser:appuser . .
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
USER appuser
 
EXPOSE 8000 

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "FinanceManager.wsgi:application"]