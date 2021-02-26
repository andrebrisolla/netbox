import os,django
from django.contrib.auth import get_user_model
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netbox.settings")
django.setup()

User = get_user_model()
User.objects.create_superuser('admin', 'admin@local.com', 'passw0rd')