from django.contrib import admin

# Register your models here.
from prices.models import Candlestick, Trade

admin.site.register(Candlestick)
admin.site.register(Trade)
