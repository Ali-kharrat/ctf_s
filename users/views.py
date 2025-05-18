from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Score
from .models import Flag, SubmittedFlag
from django.contrib import messages




def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')
    
    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'breakingbad/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'breakingbad/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def dashboard_view(request):
    try:
        user_score = Score.objects.get(user=request.user)
    except Score.DoesNotExist:
        user_score = Score.objects.create(user=request.user, points=0)
    
    top_scores = Score.objects.select_related('user').order_by('-points', 'last_submit')[:10]
    
    return render(request, 'breakingbad/dashboard.html', {
        'top_scores': top_scores,
        'user_score': user_score
    })
    
    

@login_required
def submit_flag(request):
    if request.method == "POST":
        flag_input = request.POST.get('flag')
        try:
            flag_obj = Flag.objects.get(name=flag_input)
            already_submitted = SubmittedFlag.objects.filter(user=request.user, flag=flag_obj).exists()
            if not already_submitted:
                SubmittedFlag.objects.create(user=request.user, flag=flag_obj)
                score, created = Score.objects.get_or_create(user=request.user)
                score.points += flag_obj.points
                score.save()
                messages.success(request, f"✅ Correct flag! You earned {flag_obj.points} points.")
            else:
                messages.warning(request, "⚠️ You have already submitted this flag.")
        except Flag.DoesNotExist:
            messages.error(request, "❌ Invalid flag. Try again!")
    return redirect('dashboard')






