from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import Product
from .forms import ProductForm


def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('products:create')
        form.add_error(None,"You Must be logged in to create products.")
    context = {
        'form': form
    }
    return render(request, 'pages/product-create.html', context)


def product_list(request):
    products = Product.objects.all().order_by('-updated')
    return render(request, "pages/product-list.html", {"products":products})


def product_detail(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    is_owner= False
    context = {
        'obj':obj
    }
    
    if request.user.is_authenticated:
        is_owner = obj.user == request.user
    
    if is_owner:
        form = ProductForm(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
        context['form'] = form
    
    
    return render(request, "pages/product-details.html", context)