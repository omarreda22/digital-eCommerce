import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import Product, ProductImages
from .forms import ProductForm, ProductAttachmentInlineFormSet


def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect(obj.get_manager_url)
        form.add_error(None,"You Must be logged in to create products.")
    context = {
        'form': form
    }
    return render(request, 'pages/product-create.html', context)


def product_list(request):
    products = Product.objects.all().order_by('-updated')
    return render(request, "pages/product-list.html", {"products":products})


def product_manager(request, handle=None):
    product = get_object_or_404(Product, handle=handle)
    attachements = ProductImages.objects.filter(product=product)
    is_manager = False
    context = {
        'obj':product
    }
    
    if request.user.is_authenticated:
        is_manager = product.user == request.user
    
    if not is_manager:
        return HttpResponseBadRequest()

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    formset = ProductAttachmentInlineFormSet(request.POST or None, request.FILES or None, queryset=attachements)
    if form.is_valid() and formset.is_valid() :
        obj = form.save(commit=False)
        obj.save()
        formset.save(commit=False)
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachement_obj = _form.save(commit=False)
            except:
                attachement_obj = None

            if is_delete:
                if attachement_obj is not None:
                    if attachement_obj.pk:
                        attachement_obj.delete()
            else:
                if attachement_obj is not None:
                    attachement_obj.product = obj
                    attachement_obj.save()
        return redirect(obj.get_manager_url)
    
    context['form'] = form
    context['formset'] = formset
    return render(request, "pages/product-manager.html", context)


def product_detail(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    # attachements = ProductImages.objects.filter(product=obj)
    attachements= obj.productimages_set.all()
    user = request.user
    is_owner= False
    
    if request.user.is_authenticated:
        is_owner = user.order_set.all().filter(product=obj, completed=True).exists()
    
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