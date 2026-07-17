from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404
from .forms import TaskForm, RegisterForm
from . models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Signed In!!')
        return redirect
    
    form = RegisterForm()
    errors = None

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account Created and Login Successfull!!')
                return redirect('home')
            else:
                errors = form.errors.as_data()
                messages.error(request, errors)
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)

            return redirect('register')

    context = {
        'form': form, 
        'errors': errors,
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def home(request):
    date = datetime.datetime.now()
    h = int(date.strftime('%H'))

    msg = 'Good '

    if h < 12:
        msg += 'Morning'
    elif h < 16:
        msg += 'Afternoon'
    elif h < 18:
        msg += 'Evening'
    else:
        msg += 'Night'

    greeting = f'{msg}! {request.user.username}'

    task = Task.objects.filter(user=request.user).order_by('-created_at')
    #Read everything

    context = {
        'greeting':greeting,
        'tasks' : task
    }

    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'Authentication Successful')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('login')


@login_required(login_url='login')
def add_task(request):
    forms = TaskForm()
    if request.method == 'POST':
       forms = TaskForm(request.POST)

       #===========================#
       # check for form validation#
       # =========================#
       if forms.is_valid():
            instance =  forms.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Task Added Successfully')
            return redirect('home')
       
       else:
            errors = forms.errors.as_data()
            messages.error(request, errors)
            return redirect('add_task')
    
    context = {
        'forms':forms
    }

    return render(request, 'add_task.html', context)



@login_required(login_url='login')
def filter_tasks(request, foo):
    if foo == 'true':
        tasks = Task.objects.filter(done=True).order_by('-created_at')
    elif foo == 'false':
        tasks = Task.objects.filter(done=False, user=request.user).order_by('-created_at')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'tasks': tasks
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def update_task(request, pk):
    #task = Task.objects.get(id=pk)
    task = get_object_or_404(Task, id=pk, user=request.user)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task Updated Successfully')
            return redirect('home')
        
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)
            return redirect('task', pk=pk)

        
    

    context = {
        'task': task,
        'form': form
    }
 
    return render(request, 'update_task.html', context)

@login_required(login_url='login')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    messages.success(request, 'Task Deleted')
    return redirect('home')


    






