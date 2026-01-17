# Python resmi imajını kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli paketleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Statik dosyaları topla
RUN python manage.py collectstatic --noinput

# Admin kullanıcı oluştur
RUN python create_admin.py

# Uygulama portunu belirt
EXPOSE 8000

# Gunicorn ile uygulamayı çalıştır
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wosvcore.wsgi:application"]
