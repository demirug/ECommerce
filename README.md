# ECommerce service

This service creating ecommerce with modular payment/delivery systems

You can manage constants to enable/disable system

Integrated payments:
 * PayPal
 * LiqPay
 * PayMentOnDelivery (No Payment)

Integrated delivery systems:
* NoDelivery
* NovaPoshta

___

## Installing
Client is based on `python 3.9`

To install dependencies use `pipenv` tool and run `pipenv install`

Required to be installed any chrome webdriver to parse alert data

### Setup  .env file

```
DEBUG=1
ALLOWED_HOSTS=*
SECRET_KEY=ewnc=your_project_secret_key

REDIS_HOST=127.0.0.1
REDIS_PORT=6379

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_LOGIN=my@gmail.com
PASSWORD=email_pswd
FROM_EMAIL=my@gmail.com

NOVAPOSHTA_KEY=novaposhta_api_key
NOVAPOSHTA_DEFAULT=from_warehouse_uuid

LIQPAY_PUBLIC_KEY=liq_pay_public
LIQPAY_PRIVATE_KEY=liq_pay_private

PAYPAL_CLIENT=my_paypal_client
PAYPAL_PASSWORD=my_paypal_password
```

___

### Celery
Also required celery worker. Run it by ```celery -A app.celery worker```
___