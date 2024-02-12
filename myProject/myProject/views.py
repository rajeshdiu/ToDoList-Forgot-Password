
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from myProject.forms import *
from django.contrib import messages
from datetime import date
from django.db.models import Q
from myProject.settings import EMAIL_HOST_USER
import random 
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from myApp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from notifications.signals import notify



def forget_pass(request):
    if request.method == "POST":
        my_email = request.POST.get("email")
        user = Custom_User.objects.get(email = my_email )
        otp = random.randint(111111,999999)
        user.otp_token = otp
        user.save()
        
        sub = f""" Your OTP : {otp}"""
        msg = f"Your OTP is {otp} , Keep it secret "
        from_mail = EMAIL_HOST_USER
        receipent = [my_email]
        print(user)
        print(receipent)
        print(from_mail)
        
        send_mail(
            subject= sub,
            recipient_list= receipent,
            from_email= from_mail,
            message= msg ,
        )
        return render(request,'updatepass.html',{'email':my_email})

    return render(request, "forgetpass.html")

def update_pass(request):
    if request.method=="POST":
        mail = request.POST.get('email') 
        otp = request.POST.get('otp') 
        password = request.POST.get('password') 
        c_password = request.POST.get('c_password') 
        
        print(mail,otp,password,c_password)

        user = Custom_User.objects.get(email=mail)
        print(user)
        if user.otp_token!= otp :
            return redirect('forget_pass')
        
        if password!= c_password:
            return redirect('forget_pass')
        
        user.set_password(password) 
        user.otp_token = None 
        user.save()
        print(user)
        return redirect ('mySigninPage')

    return render(request, 'updatepass.html')



def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)
    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('mySigninPage')
    
    print("account activation: ", account_activation_token.check_token(user, token))
    return redirect('mySigninPage')


def activateEmail(request,user,to_mail):
    mail_sub='Please Active Your User Account'
    user=request.user
    username=user.username
    domain=get_current_site(request).domain
    uid=urlsafe_base64_encode(force_bytes(user.pk))
    token=account_activation_token.make_token(user)
    protocol= 'https' if request.is_secure() else 'http'
    context={
        'username': username,
        'domain':domain,
        'uid':uid,
        'token':token,
        'protocol':protocol
    }
    message=render_to_string("template_activate.html",context)
    
    email= EmailMessage(mail_sub, message, to=[to_mail])
    
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')
        


def Category_List(request):
    categories=TaskCategory.objects.all()
    
    
    
    return render(request,'Category_List.html',{'categories':categories})

def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('mySigninPage')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signupPage.html', {'form': form})

def mySigninPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashBoardPage')
    else:
        form = AuthenticationForm()

    return render(request, 'loginPage.html', {'form': form})

def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('mySigninPage')

def dashBoardPage(request):
    total_tasks = myTaskModel.objects.all().count()
    completed_tasks = myTaskModel.objects.filter(completed=True).count()
    upcoming_tasks = myTaskModel.objects.filter(completed=False, due_date__gt=date.today()).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'dashBoardPage.html',context)

def create_taskPage(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            notify.send(task, task=task)
            return redirect('task_listPage')
    else:
        form = TaskForm()

    return render(request, 'create_taskPage.html', {'form': form})

def task_listPage(request):
    tasks=myTaskModel.objects.all()
    categories = TaskCategory.objects.all()

    return render(request,'task_listPage.html',{'tasks':tasks,'categories':categories})

def create_categoryPage(request):
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            notify.send(category, category=category)
            return redirect('task_listPage')
    else:
        form = TaskCategoryForm()

    return render(request, 'create_category.html', {'form': form})


def edit_categoryPage(request, category_id):
    category = get_object_or_404(TaskCategory, id=category_id)
    
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('task_listPage')  
    else:
        form = TaskCategoryForm(instance=category)

    return render(request, 'editcategory.html', {'form': form})
def delete_categoryPage(request, category_id):
    category = get_object_or_404(TaskCategory, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('task_listPage') 
    return render(request, 'delete_category.html', {'category': category}) 


def taskEditPage(request, myid):
    task = get_object_or_404(myTaskModel, id=myid)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task) 
        if form.is_valid():
            form.save()
            return redirect("task_listPage")

    else:
        form = TaskForm(instance=task) 

    return render(request, 'taskEdit.html', {'form': form})

def taskDeletePage(request, myid):
    myTaskModel.objects.filter(id=myid).delete()
    messages.success(request, 'Task Delete Successfully!')

    return redirect('task_listPage')


def TaskCompleteViewPage(request, myid):
    task = get_object_or_404(myTaskModel, pk=myid, user=request.user)
    
    if task:
        task.completed = True
        task.save()
        messages.success(request, 'Task completed successfully!')
        return redirect('task_listPage')
    else:
        messages.error(request, 'Task not found.')
        return redirect('task_listPage')

def searchTaskPage(request):
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    tasks = myTaskModel.objects.all()

    if category_filter:
        tasks = tasks.filter(category__id=category_filter)

    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    categories = TaskCategory.objects.all()

    return render(request, 'searchTaskPage.html', {'tasks': tasks, 'categories': categories})


def notifications_page(request):
  
    return render(request, 'notifications.html')