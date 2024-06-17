from rest_framework import serializers
from .models import Todo_Item

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo_Item
        fields = ['id','content','due_date']