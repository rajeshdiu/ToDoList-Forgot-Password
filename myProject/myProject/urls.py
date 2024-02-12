
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    dashBoardPage,
    mySigninPage,
    signupPage,
    logoutPage,
    create_taskPage,
    task_listPage,
    create_categoryPage,
    taskEditPage,
    TaskCompleteViewPage,
    taskDeletePage,
    searchTaskPage,
    edit_categoryPage, 
    delete_categoryPage,
    Category_List,
    forget_pass,
    update_pass,
    notifications_page,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signupPage, name='signupPage'),
    path('logoutPage/', logoutPage, name='logoutPage'),
    path('mySigninPage/', mySigninPage, name='mySigninPage'),
    path('dashBoardPage/', dashBoardPage, name='dashBoardPage'),
    path('create_taskPage/', create_taskPage, name='create_taskPage'),
    path('searchTaskPage/', searchTaskPage, name='searchTaskPage'),
    path('task_listPage/', task_listPage, name='task_listPage'),
    path('create_categoryPage/', create_categoryPage, name='create_categoryPage'),
    path('Category_List/', Category_List, name='Category_List'),
    path('taskDeletePage/<str:myid>', taskDeletePage, name='taskDeletePage'),
    path('taskEditPage/<str:myid>', taskEditPage, name='taskEditPage'), 
    path('TaskCompleteViewPage/<str:myid>', TaskCompleteViewPage, name='TaskCompleteViewPage'),
    path('edit-category/<int:category_id>/', edit_categoryPage, name='edit_categoryPage'),
    path('delete-category/<int:category_id>/', delete_categoryPage, name='delete_categoryPage'),
    path('notifications_page/', notifications_page, name='notifications_page'),
    
    path('forget_pass/', forget_pass, name='forget_pass'),
    path('update_pass/', update_pass, name='update_pass'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
