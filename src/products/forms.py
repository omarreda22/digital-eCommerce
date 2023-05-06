from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from .models import Product, ProductImages


input_css_class = "form-control-custom mb-3"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 Chars")
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['file', 'name', 'is_free', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['is_free', 'is_active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class



ProductAttachmentModelFormSet = modelformset_factory(
    ProductImages,
    form=ProductImagesForm,
    fields = ['file', 'name', 'is_free', 'is_active'],
    extra=0,
    can_delete=True
)


ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductImages,
    form=ProductImagesForm,
    formset= ProductAttachmentModelFormSet,
    fields = ['file', 'name', 'is_free', 'is_active'],
    extra=0,
    can_delete=True
)