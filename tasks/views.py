from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
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

    greeting = f'{msg}! Divine Bethel'

    tasks = [
        {'id': 1, 'text': 'Cook rice and Stew', 'done':True},
        {'id': 2, 'text': 'Wash clothes', 'done':False},
        {'id': 3, 'text': 'Family get together', 'done':False},
        {'id': 4, 'text': 'Hit the gym', 'done':True},
        {'id': 5, 'text': 'Practice Django', 'done':True},
        {'id': 6, 'text': 'Netflix and chill', 'done':False},
    ]
    context = {
        'greeting':greeting,
        'tasks' : tasks
    }

    return render(request, 'home.html', context)

def login(request):
    return render(request, 'login.html')