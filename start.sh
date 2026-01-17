#!/bin/bash

# Veritabanı migration'larını uygula
python manage.py migrate --noinput

# Admin kullanıcı oluştur
python create_admin.py

# Gunicorn ile uygulamayı başlat
exec gunicorn --bind 0.0.0.0:8000 wosvcore.wsgi:application
