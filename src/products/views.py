import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import Product, ProductImages
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


def product_manage_detail(request, handle=None):
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


def product_detail(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    # attachements = ProductImages.objects.filter(product=obj)
    attachements= obj.productimages_set.all()
    is_owner= False
    
    if request.user.is_authenticated:
        is_owner = True
    
    context = {
        'obj':obj,
        'is_owner':is_owner,
        'attachements':attachements
    }
    return render(request, "pages/product-details.html", context)


def product_images_download(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductImages, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True # check_ownership
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb')
    filename = attachment.file.name
    content_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response