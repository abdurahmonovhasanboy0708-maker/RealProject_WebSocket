from django.db import models


class Student(models.Model):
    fullname = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    def __str__(self):
        return self.fullname


class Ball(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="ball")
    coin = models.IntegerField(default=0)  # olgan bali

    def __str__(self):
        return f"{self.student} - {self.coin}"

