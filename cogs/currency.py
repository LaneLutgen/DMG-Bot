import aiohttp
from discord.ext import commands

class CurrencyConverter(object):
    def __init__(self, bot):
        self.bot = bot
        self.currencies = None

    @commands.command(aliases=["currency","cc","cv"])
    async def convert(self, ctx, amount: float, from_currency: str, to_currency: str):
        """Converts currency."""

        # disgusting hack because async fails inside the constructor
        if not self.currencies:
            self.currencies = await self.get_currencies()

        await ctx.channel.trigger_typing()

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in self.currencies:
            await ctx.send("⚠️ Please specify a valid base currency.")
            await ctx.send("You can find a list of supported currencies here: https://free.currencyconverterapi.com/api/v6/currencies")
            return

        if to_currency not in self.currencies:
            await ctx.send("⚠️ Please specify a valid target currency.")
            await ctx.send("You can find a list of supported currencies here: https://free.currencyconverterapi.com/api/v6/currencies")
            return

        if amount <= 0:
            amount = 1

        conversion_rate = await self.get_conversion_rate(from_currency, to_currency)

        conversion_rate = list(conversion_rate.values())[0]

        conversion = round(amount * conversion_rate, 2)

        await ctx.send(f"{ctx.author.mention} 💸 {amount} {from_currency} -> {conversion} {to_currency}")

    @convert.error
    async def handle_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'amount':
                await ctx.send("⚠️ You forgot the amount to convert!")
            elif error.param.name == "from_currency":
                await ctx.send("⚠️ Please specify the base currency.")
            elif error.param.name == "to_currency":
                await ctx.send("⚠️ Please specify the target currency.")

    async def get_conversion_rate(self, from_currency, to_currency):
        url = "https://free.currencyconverterapi.com/api/v6/convert"

        payload = {"q": f"{from_currency}_{to_currency}", "compact": "ultra"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as r:
                if r.status == 200:
                    js = await r.json()
                    return js
                else:
                    return None

    async def get_currencies(self):
        url = "https://free.currencyconverterapi.com/api/v6/currencies"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()
                    return js["results"]
                else:
                    return None

def setup(bot):
    bot.add_cog(CurrencyConverter(bot))