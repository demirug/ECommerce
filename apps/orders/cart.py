from django.core.handlers.wsgi import WSGIRequest

from apps.products.models import Product


def cart_option(func):
    func.__dict__['cart'] = True
    return func


class Cart:
    def __init__(self, request: WSGIRequest):
        self.session = request.session
        # Product_ID, quantity
        cart_items = {}
        if self.session.get('CART'):
            cart_items = self.session['CART']
        self.cart_items = cart_items

    @cart_option
    def add(self, product: Product, amount, save=True):
        key = str(product.pk)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] += amount

        if self.cart_items[key] > product.count:
            self.cart_items[key] = product.count

        if save:
            self.save()

    @cart_option
    def remove(self, product: Product, amount, save=True):
        key = str(product.pk)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] -= amount

        if self.cart_items[key] <= 0:
            del self.cart_items[key]

        if save:
            self.save()

    @cart_option
    def set(self, product: Product, amount, save=True):
        key = str(product.pk)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] = amount

        if self.cart_items[key] > product.count:
            self.cart_items[key] = product.count

        if self.cart_items[key] <= 0:
            del self.cart_items[key]

        if save:
            self.save()

    @cart_option
    def set_id(self, product_id, amount, save=True):
        key = str(product_id)
        self.cart_items.setdefault(key, 0)
        self.cart_items[key] = amount

        if self.cart_items[key] <= 0:
            del self.cart_items[key]

        if save:
            self.save()

    def updateQuantity(self):
        """
        Update quantity from database
        :return Products QuerySet
        """
        keys = set(self.cart_items.keys())
        products = Product.objects.filter(pk__in=self.cart_items.keys(), enable=True)
        for product in products:
            keys.remove(str(product.pk))
            self.set(product, self.cart_items[str(product.pk)], False)
        for key in keys:
            del self.cart_items[key]
        self.save()

    def clear(self):
        self.cart_items.clear()
        self.save()

    def save(self):
        self.session['CART'] = self.cart_items
        self.session.modified = True
