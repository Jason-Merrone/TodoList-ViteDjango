from django.shortcuts import render
from django.conf  import settings
import json
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .models import Todo_Item
from .serializers import TodoSerializer

# Load manifest when server launches
MANIFEST = {}
if not settings.DEBUG:
    f = open(f"{settings.BASE_DIR}/core/static/manifest.json")
    MANIFEST = json.load(f)

# Create your views here.
@login_required
def index(req):
    context = {
        "asset_url": os.environ.get("ASSET_URL", ""),
        "debug": settings.DEBUG,
        "manifest": MANIFEST,
        "js_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["file"],
        "css_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["css"][0]
    }
    return render(req, "core/index.html", context)

@login_required
def create_todo(req):
    if req.method == 'POST':
        data = JSONParser().parse(req)
        serializer = TodoSerializer(data=data)
            
        if serializer.is_valid():
            serializer.save(user=req.user)
            return JsonResponse({"todo created ":serializer.data}, status=201)
        
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def get_todos(req):
    if req.method == 'GET':
        todos = Todo_Item.objects.filter(user=req.user).order_by('-id')
        serializer = TodoSerializer(todos,many=True)
        return JsonResponse({"todos":serializer.data})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
@api_view(['put'])
def update_todo(request, todo_id): 
    try:
        todo = Todo_Item.objects.get(id=todo_id)
    except Todo_Item.DoesNotExist:
        return JsonResponse({"error": "Todo not found"}, status=404)
        
    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Todo Updated", safe=False)
        else:
            return JsonResponse("An error occurred", safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def get_todo(req, todo_id):
    if(req.method == "GET"):
        try:
            todo = Todo_Item.objects.get(id=todo_id)
            serializer = TodoSerializer(todo)
        except Todo_Item.DoesNotExist:
            return JsonResponse({"error": "Todo not found"}, status=404)
        return JsonResponse({"todo":serializer.data})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def delete_todo(req, todo_id):
    if(req.method == "POST"):
        try:
            todo = Todo_Item.objects.get(id=todo_id)
        except Todo_Item.DoesNotExist:
            return JsonResponse({"error": "Todo not found"}, status=404)
        todo.delete()
        return JsonResponse({"message": "Todo deleted"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)