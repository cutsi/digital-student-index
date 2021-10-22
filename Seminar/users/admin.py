from django.contrib import admin
from .models import korisnici
# Register your models here.
admin.site.register(korisnici)


"""
INSERT INTO
users_korisnici (id,email,password,role,status,username,is_staff,is_active,is_superuser,first_name,last_name,date_joined)
VALUES
(4, 'izv@oss.hr', '$2y$10$1SHubXN9y9sMnnLLuRPEbOyHh2xzeCpDBM8ioJgIGLuohOivnh7q6', 'student', 'izvanredni', 'izvanredni', 0, 1, 0, 'izvanredni', 'izvanredni', datetime());"""