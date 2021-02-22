from bot.bot_command_handler import BaseCommandHandler
from trades.models import Currency


class DeusCommandHandler(BaseCommandHandler):
    supported_commands = ['/deus']

    def handle(self, client, message):
        chat_id = message.chat.id

        currency = Currency.objects.get(symbol='dea')
        last_trade = currency.trades.latest('timestamp')
        message = (
                "⚡️This price is based of the last mint/burn of $DEUS⚡️"
                "\n💥So fresh from the <a href='deus.finance'>Bounding-Curve</a>💹"
                "\n📜<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS Contract</a>📜"
                "\n\n⬇️⬇️⬇️⬇️⬇️"
                "\nActual price: " + str(round(last_trade.eth_price, 4)) +
                " <a href='https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'>ETH</a> ($" +
                str(round(last_trade.usd_price, 2)) +
                ", timestamp: " +
                str(last_trade.timestamp) +
                ")" "\n⬆️⬆️⬆️⬆️⬆️"
                "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>UNISWAP</a>"
        )

        self.app.send_message(
            chat_id,
            message,
            disable_web_page_preview=True
        )
