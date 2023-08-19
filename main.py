import discord
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
import json
import pandas as pd
from datetime import datetime
import requests
from discord.ext import commands 

cg = CoinGeckoAPI()
client = discord.Client()
bot = commands.Bot(command_prefix="$")
repository = "https://github.com/ColdBio/Simple-Crypto-Dicord-Bot"

response = requests.get("https://newsapi.org/v2/everything?q=crypto&apiKey={insert your own api key}")
data = json.loads(response.text)

all_articles = data['articles']

def get_crypto_chart(token):
        chart_data = cg.get_coin_market_chart_by_id(id=f'{token}', vs_currency='gbp', days='7')

        def unix_to_date(unix_time):
            timestamp = datetime.fromtimestamp((unix_time/1000))
            return f"{timestamp.strftime('%d-%m-%Y %H:%M:%S')}"


        new_data = {}

        for each in chart_data['prices']:
            date = unix_to_date(each[0])
            new_data[date] = each[1]

        df = pd.DataFrame({'Dates': new_data.keys(), 'Prices': new_data.values()})
        print(df.head())

        df.plot(x ='Dates', y='Prices', kind = 'line', legend = None)	
        plt.axis('off')
        plt.title(f'7-day historical market price of {token}', fontsize=15, color= 'white', fontweight='bold');


        filename =  "/Users/coldbio/Desktop/test.png"
        plt.savefig(filename, transparent=True)

        plt.close()




class Coin:
    def __init__(self, name):
        self.name = name.lower()
        
        self.coin_data = cg.get_coins_markets(vs_currency='gbp', ids=f'{self.name}')
        
        self.coin_name = self.coin_data[0]['name']
        self.coin_image = self.coin_data[0]["image"]
        self.coin_price = "£{:,}".format(self.coin_data[0]['current_price'])

        self.coin_circulating_supply = "{:,}".format(self.coin_data[0]["circulating_supply"])
        self.coin_market_cap = "{:,}".format(self.coin_data[0]['market_cap'])

        self.coin_high_24h = "£{:,}".format(self.coin_data[0]['high_24h'])
        self.coin_low_24h = "£{:,}".format(self.coin_data[0]['low_24h'])

        self.coin_price_change_percent = "{:,}%".format(round(self.coin_data[0]['price_change_percentage_24h'], 2))
        
        self.coin_ath_price = "£{:,}".format(self.coin_data[0]["ath"])
        self.coin_ath_change_percent = "{:,}%".format(self.coin_data[0]["ath_change_percentage"])
        self.coin_atl = "£{:,}".format(self.coin_data[0]["atl"])



btc = Coin('bitcoin')
xrp = Coin('ripple')
eth = Coin('ethereum')
link = Coin('chainlink')
avax = Coin('avalanche-2')
ada = Coin('cardano')
vet = Coin('vechain')
doge = Coin('dogecoin')
filecoin = Coin('filecoin')
qnt = Coin('quant-network')
algo = Coin('algorand')


trending_data = cg.get_search_trending()
trending_tokens = []
count_1 = 1
for each in trending_data["coins"]:
    item = each["item"]["name"]
    trending_tokens.append(f"({count_1}). {item} \n")
    count_1 += 1

trending_coins = ''.join(trending_tokens)

market_percent_data = cg.get_global()
upcoming_ico_data = None
ongoing_ico_data = None
ended_ico_data = None

upcoming_ico_data = market_percent_data["upcoming_icos"]
ongoing_ico_data = market_percent_data["ongoing_icos"]
ended_ico_data = market_percent_data["ended_icos"]


market_cap_percentage_data = cg.get_search_trending()
market_cap_percentage = []
count_2 = 1
for k, v in market_percent_data["market_cap_percentage"].items():
    market_cap_percentage.append(f"({count_2}). {k}: {round(v, 2)}% \n")
    count_2 += 1
market_dom = ''.join(market_cap_percentage)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Converts user's input into a lowercase form
    message.content = message.content.lower().replace(' ', '')
    
    if message.author == client.user:
        return

    if message.content.startswith("$help"):
        await message.channel.send("""
        The following crypto prices are available, btc, eth, xrp, link, vet, dogecoin, ada, and avax.
        To get the price of your chosen coin/token, simply place '$' before the abbreviated name of your token. For example $eth
        List of available commands:
        $trending""")

    if message.content.startswith("$trending"):
        await message.channel.send(f"Top 7 trending search coins\n-------------------------------------\n{trending_coins}")

    if message.content.startswith("$market_dominance"):
        await message.channel.send(f"Market Cap Percentage\n-------------------------------------\n{market_dom}")
        
    if message.content.startswith("$about"):
        await message.channel.send(f"Thank you for using this discord bot.\nTo view how I was made visit here: {repository}")


    # New feature:- Return the top 5 news articles related to crypto from the NewAPI.
    # One small issue is that the articles will remain the same until the bot is reloaded.
    # Once reloadedm it fetches new articles if there are any from the API
    if message.content.startswith('$news'):
        count = 0
        await message.channel.send(f"Hey! {author.user.name}, check your DMs for the todays Top 5 news articles")
        for each in all_articles:
            count += 1
            await message.author.send(f"**{count}:- {each['title']}**\n*{each['content']}*\n{each['url']}")
            if count == 5:
                break
    

    if message.content.startswith('$btc'):
        get_crypto_chart('bitcoin')
        
        #### Create the initial embed object ####
        embed=discord.Embed(title=f"{btc.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{btc.coin_image}")

        embed.add_field(name="Current Price 💵", value=btc.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= btc.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{btc.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= btc.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= btc.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= btc.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= btc.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= btc.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = btc.coin_atl, inline=True)
        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$xrp'):
        get_crypto_chart('ripple')
        

        #### Create the initial em 
        embed=discord.Embed(title=f"{xrp.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{xrp.coin_image}")

        embed.add_field(name="Current Price 💵", value= xrp.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= xrp.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{xrp.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= xrp.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= xrp.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= xrp.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= xrp.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= xrp.coin_ath_change_percent , inline=True)
        embed.add_field(name="ATL 😢", value = xrp.coin_atl, inline=True)
        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")


        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$eth'):
        get_crypto_chart('ethereum')
        
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{eth.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{eth.coin_image}")

        embed.add_field(name="Current Price 💵", value = eth.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= eth.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{eth.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= eth.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= eth.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= eth.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= eth.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= eth.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = eth.coin_atl, inline=True)
        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)

    
    if message.content.startswith('$link'):
        get_crypto_chart('chainlink')
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{link.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{link.coin_image}")

        embed.add_field(name="Current Price 💵", value= link.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= link.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{link.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= link.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= link.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= link.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value=link.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value=link.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = link.coin_atl, inline=True)

        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)
    
    if message.content.startswith('$ada'):
        get_crypto_chart('cardano')
        
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{ada.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{ada.coin_image}")

        embed.add_field(name="Current Price 💵", value= ada.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= ada.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{ada.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= ada.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= ada.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= ada.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= ada.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= ada.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = ada.coin_atl, inline=True)
        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$avax'):
        get_crypto_chart('avalanche-2')
        
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{avax.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{avax.coin_image}")

        embed.add_field(name="Current Price 💵", value= avax.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= avax.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{avax.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= avax.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= avax.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= avax.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= avax.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= avax.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = avax.coin_atl, inline=True)
        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)

    if message.content.startswith('$doge'):
        get_crypto_chart('dogecoin')
        
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{doge.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{doge.coin_image}")

        embed.add_field(name="Current Price 💵", value= doge.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= doge.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{doge.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= doge.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= doge.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= doge.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= doge.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= doge.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = doge.coin_atl, inline=True)
        
        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)
    
    if message.content.startswith('$vet'):
        get_crypto_chart('vechain')
        
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{vet.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{vet.coin_image}")

        embed.add_field(name="Current Price 💵", value= vet.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= vet.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{vet.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= vet.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= vet.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= vet.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= vet.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= vet.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = vet.coin_atl, inline=True)

        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)

    
    if message.content.startswith('$filecoin'):
        get_crypto_chart('filecoin')
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{filecoin.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{filecoin.coin_image}")

        embed.add_field(name="Current Price 💵", value= filecoin.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= filecoin.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{filecoin.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= filecoin.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= filecoin.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= filecoin.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= filecoin.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= filecoin.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = filecoin.coin_atl, inline=True)

        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)


    
    if message.content.startswith('$qnt'):
        get_crypto_chart('quant-network')
        
        #### Create the initial embed object #eth
        embed=discord.Embed(title=f"{qnt.coin_name}")

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name=f"{client.user.name}", icon_url=client.user.avatar_url)

        embed.set_thumbnail(url=f"{qnt.coin_image}")

        embed.add_field(name="Current Price 💵", value= qnt.coin_price, inline=True)
        embed.add_field(name="Circulating Supply 🪙", value= qnt.coin_circulating_supply, inline=True)
        embed.add_field(name="Market Cap 🤑", value= f"£{qnt.coin_market_cap}", inline=True)

        embed.add_field(name="24h-High ⬆️", value= qnt.coin_high_24h, inline=True)
        embed.add_field(name="24h-low ⬇️", value= qnt.coin_low_24h, inline=True)
        embed.add_field(name="Price Change 24h ⏰", value= qnt.coin_price_change_percent, inline=True)

        embed.add_field(name="All Time High 👑", value= qnt.coin_ath_price, inline=True)
        embed.add_field(name="ATH Percent Change 📊", value= qnt.coin_ath_change_percent, inline=True)
        embed.add_field(name="ATL 😢", value = qnt.coin_atl, inline=True)

        file = discord.File("/Users/coldbio/Desktop/test.png", filename="image.png")

        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="Thank you for using Crypto Bot Price Checker 🙏")

        await message.channel.send(file=file, embed=embed)


client.run("{insert your own bot token here}")
