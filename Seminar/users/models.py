from django.db import models
from django.contrib.auth.models import User, AbstractUser


class predmeti(models.Model):
    DA = "da"
    NE = "ne"
    ime = models.CharField(max_length=255)
    kod = models.CharField(max_length = 16)
    program = models.TextField()
    bodovi = models.IntegerField()
    sem_redovni = models.IntegerField()
    sem_izvanredni = models.IntegerField()
    IZBORNI_CHOICES = [
        (DA, 'Ne'), 
        (NE, 'Da'),
    ]
    izborni = models.CharField(
        max_length=10,
        choices=IZBORNI_CHOICES,
        default=NE,
    )

class korisnici(AbstractUser):

    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=128)
    
    MENTOR = "mentor"
    STUDENT = "student"
    ROLE_CHOICES = [
        (MENTOR, "Mentor"),
        (STUDENT, "Student"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )

    NONE = "none"
    REDOVNI = "redovni"
    IZVANREDNI = "izvanredni"
    	
    STATUS_CHOICES = [
        (NONE, "None"),
        (REDOVNI, "Redovni"),
        (IZVANREDNI, "Izvanredni"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=REDOVNI,
    )

class upis(models.Model):
    student_id = models.ForeignKey(korisnici, on_delete=models.CASCADE, default = "null")
    predmet_id = models.ForeignKey(predmeti, on_delete=models.CASCADE, default = "null")
    status = models.CharField(max_length=64)

    

