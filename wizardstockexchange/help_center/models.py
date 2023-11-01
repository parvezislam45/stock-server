from django.db import models
from django.utils import timezone
# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    def __str__(self):
        return self.email  # Display the email in the admin panel
    
class LiveChatMessage(models.Model):
    sender_name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender_name}: {self.message}"