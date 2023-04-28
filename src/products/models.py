from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save


User = settings.AUTH_USER_MODEL

class Product(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=125)
    handle = models.SlugField(null=True, blank=True, unique=True)
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
        return f"/products/{self.handle}"

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