# 1. İçinde hazır Python olan bir bilgisayar getir
FROM python:3.11-slim

# 2. İçinde '/app' adında bir çalışma masası kur
WORKDIR /app

# 3. İhtiyaç listesini masaya koy ve kütüphaneleri kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Benim tüm kodlarımı ve data klasörümü kutunun içine kopyala
COPY . .

ENV PYTHONUNBUFFERED=1