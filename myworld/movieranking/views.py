from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Comment
from .forms import CommentForm, SignUpForm, ForgotPasswordForm, PasswordResetForm, SecurityQuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout 
from django.conf import settings


def index(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query) | \
                 Movie.objects.filter(genre__icontains=query) | \
                 Movie.objects.filter(release_year__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'index.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movie=movie)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.movie = movie
                comment.save()
                return redirect('movie_detail', movie_id=movie_id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments, 'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first() 

            if user:
                # Store user ID or email in session for next step
                request.session['user_email'] = email
                return redirect('security_question')
            else:
                return redirect('index')   
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

def security_question(request):
    if request.method == 'POST':
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            security_answer = form.cleaned_data['security_answer']
            user_email = request.session.get('user_email')
            user = User.objects.filter(email=user_email).first()
            if user and user.security_answer == security_answer:
                # Store user ID in session for password reset
                request.session['user_id'] = user.id
                return redirect('reset_password')
            else:
                return redirect('index') 
    else:
        form = SecurityQuestionForm()
    return render(request, 'security_question.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            # Process form data and reset password
    else:
        form = MyPasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})