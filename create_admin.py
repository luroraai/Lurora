import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wosvcore.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Admin kullanıcı bilgileri
username = 'admin'
email = 'admin@lurora.com'
password = 'Lurora2024!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully!')
else:
    print(f'Superuser {username} already exists.')