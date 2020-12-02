from django.db import models

# Create your models here.

class admin(models.Model):
    username = models.CharField(max_length=150, null=False)
    password = models.CharField(max_length=150, null=False)


class TTN(models.Model):
    ttn_no = models.CharField(max_length=150, null=False, unique=True)

class TestResults(models.Model):
    email = models.EmailField(max_length=150, null=False)
    full_name = models.CharField(max_length=150, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=150, null=False)
    address = models.TextField()
    postcode = models.CharField(max_length=150, null=False)
    ttn_code = models.OneToOneField(TTN, related_name="test_ttn", on_delete=models.CASCADE)
    test_result = models.CharField(max_length=150, null=False)

