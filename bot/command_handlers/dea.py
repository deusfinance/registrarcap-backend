import requests

from bot.bot_command_handler import BaseCommandHandler
from trades.models import Currency


class DeaCommandHandler(BaseCommandHandler):
    supported_commands = ['/dea', '/deausdc']

    def handle(self, client, message):
        chat_id = message.chat.id

        currency = Currency.objects.get(symbol='dea')
        last_trade = currency.trades.latest('timestamp')

        dea_per_usdc, usdc_per_dea = self.get_uniswap_price()
        price_eth = self.get_eth_price()
        eth_per_dea = "%.4f" % (float(usdc_per_dea) / float(price_eth))
        usdc_per_dea = "%.2f" % float(usdc_per_dea)

        message = (
                "\n📜<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA Contract</a>📜"
                "\nKeep in mind this is the "
                "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>"
                " price (not $)."
                "\nThis price is from the "
                "<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA</a>"
                " / "
                "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>"
                " pool."
                "\n\n⬇️⬇️⬇️⬇️⬇️"
                "\nActual price: {} ".format(eth_per_dea) +
                "<a href='https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'>ETH</a>"
                "\n({} ".format(usdc_per_dea) +
                "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>)"
                "\n⬆️⬆️⬆️⬆️⬆️"
                "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>UNISWAP</a>"
        )
        self.app.send_message(
            chat_id,
            message,
            disable_web_page_preview=True
        )

        message = (
                "\n📜<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA Contract</a>📜"
                "\nKeep in mind this is the $ / "
                "<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS</a>"
                " price (not "
                "<a href='https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'>USDC</a>)."
                "\nThis price is from the "
                "<a href='https://etherscan.io/token/0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>DEA</a>"
                " / "
                "<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS</a>"
                " pool."
                "\n\n⬇️⬇️⬇️⬇️⬇️"
                "\nActual price: {} ".format(round(last_trade.deus_price, 4)) +
                "<a href='https://etherscan.io/token/0x3b62F3820e0B035cc4aD602dECe6d796BC325325'>DEUS</a>"
                "\n(${})".format(round(last_trade.usd_price, 2)) +
                "\n⬆️⬆️⬆️⬆️⬆️"
                "\n\n<a href='https://app.uniswap.org/#/swap?outputCurrency=0x80ab141f324c3d6f2b18b030f1c4e95d4d658778'>UNISWAP</a>"

        )

        self.app.send_message(
            chat_id,
            message,
            disable_web_page_preview=True
        )

    def get_uniswap_price(self):
        epApiKey = 'freekey'
        interact_address = "0x83973dcaa04A6786ecC0628cc494a089c1AEe947"
        request_url = "https://api.ethplorer.io/getAddressInfo/" + str(interact_address) + "?apiKey=" + epApiKey
        res = requests.get(request_url).json()
        balance_a = float(res["tokens"][0]["balance"]) * (
                1 / 10 ** float(res["tokens"][0]["tokenInfo"]["decimals"]))
        balance_b = float(res["tokens"][1]["balance"]) * (
                1 / 10 ** float(res["tokens"][1]["tokenInfo"]["decimals"]))
        return (balance_a / balance_b), (balance_b / balance_a)

    def get_eth_price(self):
        request_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        res = requests.get(request_url).json()
        return res["ethereum"]["usd"]
