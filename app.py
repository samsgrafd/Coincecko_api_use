
# coding: utf-8

from flask import request
from flask import Flask
import requests
import json
import requests
from datetime import datetime
from datetime import timezone
from datetime import date
from datetime import timedelta
import argparse
import sys
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)


class CoinsApi(Resource):

    def get(args):
        if args.end_date - args.start_date < datetime.timedelta(days=90):
            a = True
            # The API returns daily data (00:00 UTC) if time range is above 90 days
            extended_date = args.end_date + datetime.timedelta(days=90)
        return args.response
        
    
    @classmethod
    def make_api(self, prices, volumes):
        a = False
        # check if time range is more than 90 days
        if args.end_date - args.start_date < timedelta(days=90):
            a = True
            # The API returns daily data (00:00 UTC) if time range is above 90 days
            extended_date = args.end_date + timedelta(days=90)

        try:
            url = f'https://api.coingecko.com/api/v3/coins/{args.currency.lower()}/market_chart/range?vs_currency=eur&from={args.start_date.timestamp()}&to={extended_date.timestamp() if a else args.end_date.timestamp()}'
            r = requests.get(url)
            data = json.loads(r.text)
        except requests.exceptions.RequestException as ex:
            raise SystemExit(ex)
    
        max_volume = 0
        max_volume = max(x[1] for x in volumes) #highest volume
        timestamp = [x[0] for x in volumes if x[1] == max_volume][0] # find the timestamp
        try:  # Only relevant values from the data
            if a:
                end = (extended_date-args.start_date).days - 90 + 1
                prices = data['prices'][0:end]
                volumes = data['total_volumes'][0:end]
            else:
                prices = data['prices']
                volumes = data['total_volumes']
        except KeyError:
            print('There is no prices available for that currency.')
        
        max_volume = max(x[1] for x in volumes) #highest volume
        timestamp = [x[0] for x in volumes if x[1] == max_volume][0]
        volume_date = datetime.fromtimestamp(timestamp / 1000).date() 

        print(
            f"{args.currency.title()}'s highest trading volume was {round(max_volume, 2)}€ on {volume_date}.")

        def trend(prices):
            decrease = []
            temp = 0
            for i, d in enumerate(prices):
                if i > 0: # If not first 
                    if d[1] < prices[i - 1][1]: # If price is less than the days before
                        temp += 1
                    else:
                        decrease.append(temp)
                        temp = 0

            decrease.append(temp)
            trend = max(decrease) #Return highest value
            print(f"{args.currency.title()}'s price decreased {trend} days in a row for the selected time.")
        
        trend(prices)
       
        
        def profit(prices):
            profitsellandbuy = []
            for timestamp1, price1 in prices:
                for timestamp2, price2 in prices:
                    diff = price2 - price1
                    if (diff > 0) and (timestamp1 < timestamp2):
                        profitsellandbuy.append({
                            "buy": timestamp1,
                            "sell": timestamp2,
                            "buy_price": price1,
                            "sell_price": price2,
                            "difference": diff
                        })
        
            max_diff = max(x['difference'] for x in profitsellandbuy)
            [x for x in profitsellandbuy if x['difference'] == max_diff][0]
        
            
                                  
            try:
                max_diff = max(x['difference'] for x in profitsellandbuy)
                if profitsellandbuy is not None:
                    buy_date = datetime.utcfromtimestamp(
                    profitsellandbuy[0]['buy']/1000).date()
                    sell_date = datetime.utcfromtimestamp(
                    profitsellandbuy[1]['sell']/1000).date()
                    print(
                        f"Buy {args.currency.title()} on {buy_date} and sell on {sell_date} to maximize profits.")
                else:
                    print(
                        f"You shouldn't buy or sell {args.currency.title()} on the selected time period.")
                return [x for x in profitsellandbuy if x['difference'] == max_diff][0]
            except ValueError: #shouldn't buy
                return None
                        
        profit(prices)       
          

class KillerApp():
    def __init__(self):
        self.app = Flask(__name__)
        MyApi = CoinsApi.make_api({"key": "value"}, {"key": "value"})
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description="Dates are accepted in ISO 8601 format. (YYYY-DD-MM)")
    parser.add_argument('start_date', type=datetime.fromisoformat,
                        help="Start date of the time period.")
    parser.add_argument('end_date', type=datetime.fromisoformat,
                        help="End date of the time period.")
    parser.add_argument('--currency', nargs="?", type=str,
                        help="The cryptocurrency used in the calculations. Bitcoin is used as default", default="bitcoin")
    args = parser.parse_args()

KillerApp()
