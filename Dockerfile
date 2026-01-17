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

# start.sh'a çalıştırma izni ver
RUN chmod +x start.sh

# Uygulama portunu belirt
EXPOSE 8000

# Uygulama başlatma scripti ile çalıştır
CMD ["./start.sh"]
