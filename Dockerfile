FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    kagglehub \
    pandas \
    scikit-learn \
    matplotlib \
    pytest

CMD ["python", "gold_price_analysis.py"]