# yourapp/admin.py

from django.contrib import admin
from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'completed', 'category')
    list_filter = ('user', 'completed', 'due_date', 'priority', 'category')
    search_fields = ('title', 'description', 'notes')
    date_hierarchy = 'due_date'

class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
    
class customUserDisplay(admin.ModelAdmin):
    list_display = ('username', 'user_type')

admin.site.register(Custom_User, customUserDisplay)

admin.site.register(myTaskModel, TaskAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)

