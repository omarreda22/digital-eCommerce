# Digital eCommerce
eCommerce Web App with Python and Serverless Postgres (neon)

![Micro eCommerce](https://github.com/omarreda22/digital-eCommerce/blob/main/src/core/static-files/redmi/micro-ec.PNG)

## Technology Used
- Python/Django
- TailwindCSS/Flowbite
- Neon - Serverless Postgres
- Payment Processing with Stripe
- Docker

## Steps I followed to build this project
1. Setup project and install [pip - pip-tools - rav] and using rav.yaml to write some scripts to make commands easy
2. Setup neon serverless postgres and create a product model to test the database
3. Using ".env" file, Decouple, and Dj_Database_Url to make database information secure
4. Build signals for product model to handle slugs
5. Build forms and four function based views [product_list - product_create - product_update - product_details]
6. Build pretty templates with Tailwind and Flowbite
7. Making Product Images more protected using FileSystemStorage and create new MEDIA ROOT called PROTECTED_MEDIA_ROOT
8. build a new view to handle download product attachments then display this as a table in templates with some condition
9. Building formsets for product images then making this dynamically by JavaScript Creating orders model to handle purchase products then connect with stripe checkout API and integrate Stripe with our project then build new views to handle the purchase process
10. Integrate Stripe payment to our Django Models
11. Containerize the Django App with Docker
