from webbrowser import get

from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Fruit, Category
from .forms import CategoryForm, FruitAddForm, FruitEditForm, FruitDeleteForm


# Create your views here.

def index_view(request):
    
    return render(request, 'common/index.html')

def dashboard_view(request):

    fruits = Fruit.objects.all()

    context = {'fruits': fruits}

    return render(request, 'common/dashboard.html', context)

def fruit_create_view(request):

    if request.method == 'POST':
        form = FruitAddForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = FruitAddForm()

    context = {'form': form}

    return render(request, 'fruits/create-fruit.html', context)

def fruit_details_view(request, pk):

    fruit = Fruit.objects.get(id=pk)

    context = {'fruit': fruit}

    return render(request, 'fruits/details-fruit.html', context)

def fruit_edit_view(request, pk):

    fruit = Fruit.objects.get(id=pk)

    if request.method == 'GET':
        form = FruitEditForm(instance=fruit)

    elif request.method == 'POST':
        form = FruitEditForm(request.POST, instance=fruit)

        if form.is_valid():

            fruit.save()
            return redirect('dashboard')

    context = {'form': form, 'fruit': fruit}

    return render(request, 'fruits/edit-fruit.html', context)

def fruit_delete_view(request, pk):

    fruit = Fruit.objects.get(id=pk)

    if request.method == 'GET':
        form = FruitDeleteForm(instance=fruit)

    else:
        form = FruitDeleteForm(request.POST, instance=fruit)

        if form.is_valid():

            fruit.delete()
            return redirect('dashboard')

    context = {'form': form, 'fruit': fruit}

    return render(request, 'fruits/delete-fruit.html', context)

def category_create_view(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
        
    else:
        form = CategoryForm()

    context = {'form': form}

    return render(request, 'categories/create-category.html', context)