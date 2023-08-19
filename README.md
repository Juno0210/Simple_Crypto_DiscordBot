## Simple Crypto Dicord Bot
A simple discord crypto bot that returns back the price of a limited set of cryptocurrency prices.
Currently available crypto prices:
- XRP
- Bitcoin
- Ethereum
- Chainlink
- Vechain
- Avalanche
- Cardano
- Dogecoin
- Filecoin
- Quant
- Algorand

## Motivation
I created this rather simple discord bot to provide convenient crypto related data for me and my friends on our shared discord server  

## Installation
Before running the code make sure to install the packages listed below

### Discord.py

```python 
pip3 install discord.py
```
### CoinGeko API Wrapper

```python
pip3 install pycoingecko
```

## Commands
- `$help`:- Informes the user which coins/tokens are supported and how to call their prices
- `$about`:- Where to find the source code and who the creater is
- `$trending`:- Provides the top 7 trending search coins/tokens 
- `$market_dominance`:- Returns a list of the most dominant coins in terms of overall market cap percentage
- `$news`:- Returns top 5 articles related to cryptocurrencies in to your DM (requires improvement❗️)

## Disclaimer
When calling any token, chart data is taken from the Coingecko API, plotted on a line chart, saved to the desktop, and displayed in the chosen discord chat.
While this does accomplish the desired need to display chart data for each token, it raises an unexpected issue of when two or more users call the bot at the same time, or when they call it one after another in quick succession. The image takes n-amount of time to save but when two or more commands are called, the previously saved image is returned because the the currently being saved image did not have enough time to be saved. This requires a fix and an issue should be raised.

## Demo
XRP |  Bitcoin
:-------------------------:|:-------------------------:
<img width="498" alt="Screenshot 2022-01-28 at 18 18 05" src="https://user-images.githubusercontent.com/64978825/151600552-57b17b32-fc18-4277-9cda-e0cdb7a5d677.png">|<img width="482" alt="Screenshot 2022-01-28 at 18 18 22" src="https://user-images.githubusercontent.com/64978825/151600559-514f1127-fed1-4c39-bb02-0fcfcdb68e78.png">|
