from django.contrib import admin

from trades.models import Candlestick, Trade, Currency


class TradeAdmin(admin.ModelAdmin):
    search_fields = ('id', 'timestamp', 'amount', 'hash')


admin.site.register(Currency)
admin.site.register(Candlestick)
admin.site.register(Trade, TradeAdmin)
