from django.shortcuts import render
from django.conf  import settings
import json
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Todo_Item

# # Load manifest when server launches
# MANIFEST = {}
# if not settings.DEBUG:
#     f = open(f"{settings.BASE_DIR}/core/static/manifest.json")
#     MANIFEST = json.load(f)

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
        user = req.user
        content = req.POST.get('content')
        due_date = req.POST.get('due_date')
            
        if(due_date):
            from datetime import datetime
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            except ValueError:
                return render(req, 'core/create_todo.html', {'error': 'Invalid date format. Use YYYY-MM-DD.'})
                
        new_todo = Todo_Item.objects.create(
            user = user,
            content = content,
            due_date=due_date
        )
            
        new_todo.save()
        
        return JsonResponse({"message": "Todo created successfully"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def get_todos(req):
    if req.method == 'GET':
        todos = Todo_Item.objects.filter(user=req.user).order_by('-id')
        todos_data = [
            {
                "id": todo.id,
                "content": todo.content,
                "due_date": todo.due_date
            } for todo in todos
        ]
        return JsonResponse({"Todos": todos_data})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def update_todo(req, todo_id):
    try:
        todo = Todo_Item.objects.get(id=todo_id)
    except Todo_Item.DoesNotExist:
        return JsonResponse({"error": "Todo not found"}, status=404)
    
    todo_content = req.get('content')
    if todo_content is not None:
        todo.content = todo_content
        
    todo_due_date = req.get('due_date')
    