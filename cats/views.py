from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat
from .forms import CatForm

# Create your views here.

def cat_list(request):
    cats = Cat.objects.all()
    return render(request, 'cats/cat_list.html', {'cats': cats})

def cat_detail(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    return render(request, 'cats/cat_detail.html', {'cat': cat})

def cat_create(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cat_list')
    else:
        form = CatForm()
    return render(request, 'cats/cat_form.html', {'form': form})

def cat_update(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('cat_detail', pk=pk)
    else:
        form = CatForm(instance=cat)
    return render(request, 'cats/cat_form.html', {'form': form})

def cat_delete(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    if request.method == 'POST':
        cat.delete()
        return redirect('cat_list')
    return render(request, 'cats/cat_confirm_delete.html', {'cat': cat})