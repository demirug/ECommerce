from jinja2 import Environment

from app.settings import SITE_NAME, CURRENCY_SYMBOL


def environment(**options):
    options['cache_size'] = 0
    env = Environment(**options)
    env.globals.update({
        'site_name': SITE_NAME,
        'currency_symbol': CURRENCY_SYMBOL
    })
    return env