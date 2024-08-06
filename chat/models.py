from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    allowed_users = models.ManyToManyField(User, related_name='allowed_rooms', blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"
