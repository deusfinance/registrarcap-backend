from django.contrib import admin

from trades.models import Candlestick, Trade, Currency

admin.site.register(Currency)
admin.site.register(Candlestick)
admin.site.register(Trade)
