from django.db import models
from datetime import date, timedelta
import uuid
import string
import random
import datetime

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    institution = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')
    photo = models.ImageField(upload_to='photos/')
    issuance_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    student_id = models.CharField(max_length=9, unique=True, blank=True)
    id_card = models.ImageField(upload_to='id_cards/', blank=True, null=True)

        
    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"


class StudentIdentityCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='identity_cards/', null=True, blank=True)
    image_file = models.ImageField(upload_to='identity_cards/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name}'
