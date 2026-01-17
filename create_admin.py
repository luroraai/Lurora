import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wosvcore.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Admin kullanıcı bilgileri
email = 'admin@lurora.com'
password = 'Lurora2024!'

# Mevcut admin varsa sil
User.objects.filter(email=email).delete()

# Yeni superuser oluştur
try:
    user = User.objects.create_superuser(
        email=email,
        password=password
    )
    print(f'Superuser {email} created successfully!')
except Exception as e:
    # Eğer username gerekiyorsa
    try:
        user = User.objects.create_superuser(
            username='admin',
            email=email,
            password=password
        )
        print(f'Superuser {email} created successfully with username!')
    except Exception as e2:
        print(f'Error creating superuser: {e2}')
