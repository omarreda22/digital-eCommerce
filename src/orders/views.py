import random
import stripe

from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from products.models import Product
from .models import Order
from core.env import config


STRIPE_SECRET_KEY = config("STRIP_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY
BASE_ENDPOINT= config("BASE_ENDPOINT", default="http://127.0.0.1:8000")

def orders_process_start(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()

    user = request.user
    if not user.is_authenticated:
        return HttpResponseBadRequest()

    slug = request.POST.get('handle')
    obj = Product.objects.get(handle=slug)
    stripe_price_id = obj.stripe_price_id
    if not stripe_price_id:
        return HttpResponseBadRequest()

    order = Order.objects.create(user=user, product=obj)
    request.session['order_id'] = order.id
    print(order, order.id)
    success_path = reverse("orders:order_success")
    if not success_path.startswith('/'):
        success_path = f"/{success_path}"
    cancel_path = reverse("orders:order_error")
    success_url = f"{BASE_ENDPOINT}{success_path}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"
    checout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price":stripe_price_id,
                "quantity":1
            }
        ],
        mode = "payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    print(order, order.id)
    order.stripe_checkout_session_id = checout_session.id
    order.save()
    request.session['order_id'] = order.id
    return HttpResponseRedirect(checout_session.url)


def orders_process_success(request):
    print(request.session.get('order_id'))
    order_id = request.session.get('order_id')
    print((order_id))
    if order_id:
        order = Order.objects.get(id=order_id)
        order.completed = True
        order.save()
    return HttpResponse(f"Successfuly {order_id}")


def orders_process_error(request):
    return HttpResponse("Error with this order process!")