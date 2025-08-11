from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Cat, Rating, Comment
from .forms import CatForm, RatingForm, CommentForm, CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.

def cat_list(request):
    cats = Cat.objects.all().order_by('-created_at')
    return render(request, 'cats/cat_list.html', {'cats': cats})

def cat_detail(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    comments = cat.comments.all().order_by('-created_at')
    
    # Get user's existing rating if logged in
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(cat=cat, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    rating_form = RatingForm()
    comment_form = CommentForm()
    
    context = {
        'cat': cat,
        'comments': comments,
        'user_rating': user_rating,
        'rating_form': rating_form,
        'comment_form': comment_form,
    }
    return render(request, 'cats/cat_detail.html', context)

@login_required
def cat_create(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            messages.success(request, 'Your cat has been added to the gallery!')
            return redirect('cat_detail', pk=cat.pk)
    else:
        form = CatForm()
    return render(request, 'cats/cat_form.html', {'form': form, 'title': 'Add New Cat'})

@login_required
def cat_update(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)  # Only owner can edit
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cat updated successfully!')
            return redirect('cat_detail', pk=pk)
    else:
        form = CatForm(instance=cat)
    return render(request, 'cats/cat_form.html', {'form': form, 'title': 'Edit Cat'})

@login_required
def cat_delete(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)  # Only owner can delete
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Cat deleted successfully!')
        return redirect('cat_list')
    return render(request, 'cats/cat_confirm_delete.html', {'cat': cat})

@login_required
def rate_cat(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            try:
                rating, created = Rating.objects.get_or_create(
                    cat=cat, 
                    user=request.user,
                    defaults={'score': form.cleaned_data['score']}
                )
                if not created:
                    # Update existing rating
                    rating.score = form.cleaned_data['score']
                    rating.save()
                    messages.success(request, 'Your rating has been updated!')
                else:
                    messages.success(request, 'Thank you for rating this cat!')
            except IntegrityError:
                messages.error(request, 'You have already rated this cat.')
    
    return redirect('cat_detail', pk=pk)

@login_required
def add_comment(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    
    # Check if user has rated this cat
    try:
        Rating.objects.get(cat=cat, user=request.user)
    except Rating.DoesNotExist:
        messages.error(request, 'You must rate this cat before commenting!')
        return redirect('cat_detail', pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.cat = cat
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
    
    return redirect('cat_detail', pk=pk)

@login_required
def profile(request):
    user_cats = Cat.objects.filter(owner=request.user).order_by('-created_at')
    user_comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    user_ratings = Rating.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'user_cats': user_cats,
        'user_comments': user_comments,
        'user_ratings': user_ratings,
    }
    return render(request, 'cats/profile.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Cat Gallery! You can now upload and rate cats.')
            return redirect('cat_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'cats/signup.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('cat_list')
    return render(request, 'registration/logout.html')