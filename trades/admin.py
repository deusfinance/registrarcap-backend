from django.contrib import admin

from trades.models import Candlestick, Trade, Currency


class TradeAdmin(admin.ModelAdmin):
    search_fields = ('id', 'timestamp', 'amount', 'hash', 'currency__symbol')

    def get_ordering(self, request):
        return ['-timestamp']


admin.site.register(Currency)
admin.site.register(Candlestick)
admin.site.register(Trade, TradeAdmin)
