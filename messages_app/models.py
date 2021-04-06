from django.db import models
import datetime


class User(models.Model):
    _id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender',null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver',null=True,blank=True)
    content = models.CharField(max_length=200)
    sent_time = models.DateTimeField(default=datetime.datetime.now())
    read = models.BooleanField(default=False)
    subject = models.CharField(max_length=200, default='')

    def __str__(self):
        return "message from " + self.sender.first_name + " to " + self.receiver.first_name
