from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo_Item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length = 150)
    due_date = models.DateField(blank = True, null=True)

    def __str__(self):
        return f'{self.content} (Due: {self.due_date})'