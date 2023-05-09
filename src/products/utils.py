import stripe 

from core.env import config


STRIPE_SECRET_KEY = config("STRIP_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY


def product_sales_pipeline(product_name="Test Product", product_price=1000):
    stripe_product_obj = stripe.Product.create(name=product_name)
    stripe_product_id = stripe_product_obj.id
    stripe_price_obj = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=product_price,
        currency="usd"
    )
    """
        all the top for:
            get stripe_price_obj.id from:
                stripe_product_id
                stripe_price_id
    """

    stripe_price_id = stripe_price_obj.id
    base_endpoint= "http://localhost:8000"
    success_url = f"{base_endpoint}/order/success/"
    error_url = f"{base_endpoint}/order/error/"
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {"price": stripe_price_id,
            "quantity": 1}
        ],
        mode="payment",
        success_url = success_url,
        cancel_url=error_url
    )
    print(checkout_session)