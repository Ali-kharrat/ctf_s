from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_submit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} pts"


class Flag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # مثلاً Flag{level1}
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class SubmittedFlag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'flag')  
    def __str__(self):
        return f"{self.user.username} - {self.flag.name}"