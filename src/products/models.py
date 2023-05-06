import pathlib

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.files.storage import FileSystemStorage
from django.urls import reverse



User = settings.AUTH_USER_MODEL
PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=125)
    handle = models.SlugField(null=True, blank=True, unique=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99) 
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    strip_price = models.IntegerField(default=999) # price * 100
    proice_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.price != self.og_price:
            # price Changed
            self.og_price = self.price
            self.strip_price = int(self.price * 100)
            self.proice_changed_timestamp = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:details", kwargs={"handle": self.handle})

    
    @property
    def get_manager_url(self):
        return reverse("products:manager", kwargs={"handle": self.handle})

    def __str__(self):
        return self.name[:20]


def slug_handle(sender, instance, *args, **kwargs):
    if instance.handle is None or instance.handle == '':
        new_slug = slugify(instance.name)
        klass = instance.__class__
        qs = klass.objects.filter(handle__icontains=new_slug).exclude(id=instance.id)
        if qs.count() == 0:
            instance.handle = new_slug
        else:
            instance.handle = f'{new_slug}-{qs.count()}'

pre_save.connect(slug_handle, sender=Product)


def handle_product_images_upload(instance, filename):
    return f"products/{instance.product.handle}/images/{filename}"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_images_upload, storage=protected_storage)
    name = models.CharField(max_length=125, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.handle
    

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = pathlib.Path(self.file.name).name

        super().save(*args, **kwargs)

    @property
    def get_name(self):
        return self.name or pathlib.Path(self.file.name).name

    def get_download_url(self):
        return reverse("products:download", kwargs={"handle":self.product.handle, "pk":self.id})
    