
# coding: utf-8

from flask import request
from flask import Flask
import requests
import json
from datetime import datetime, timezone, date
from datetime import timedelta
import argparse
import sys
from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser


app = Flask(__name__)


app.secret_key = "secret key"


api = Api(app)


    
def main(args):
    if args.date_to < args.date_from:
        exit()

   

def downward_trend(prices):
    decrease = []
    temp = 0
    for i, d in enumerate(prices):
        if i > 0: # If not first one
            if d[1] < prices[i - 1][1]: # If price is less than the days before
                temp += 1
            else:
                decrease.append(temp)
                temp = 0

    decrease.append(temp)
    return max(decrease) #Return highest value


def trading_volume(volumes):
    max_volume = max(x[1] for x in volumes) #highest volume
    timestamp = [x[0] for x in volumes if x[1] == max_volume][0] # find the timestamp

    return timestamp, max_volume


def best_profit(prices):
    profit = []
    for timestamp1, price1 in prices:
        for timestamp2, price2 in prices:
            diff = price2 - price1
            if (diff > 0) and (timestamp1 < timestamp2):
                profit.append({
                    "buy": timestamp1,
                    "sell": timestamp2,
                    "buy_price": price1,
                    "sell_price": price2,
                    "difference": diff
                })
    try:
        max_diff = max(x['difference'] for x in profit)
        return [x for x in profit if x['difference'] == max_diff][0]
    except ValueError: #shouldn't buy
        return None


    trend = downward_trend(prices) #Get the maximum downward trend

    return(
        f"{args.currency.title()}'s price decreased {trend} days in a row for the selected time range.")

    timestamp, max_volume = trading_volume(volumes) # Get highest trading volume
    volume_date = datetime.datetime.utcfromtimestamp(timestamp / 1000).date() # Convert UNIX timestamp to a date

    return(
        f"{args.currency.title()}'s highest trading volume was {round(max_volume, 2)}€ on {volume_date}.")

    profit = best_profit(prices) # Get most profitable days and prices
    if profit is not None:
        buy_date = datetime.datetime.utcfromtimestamp(
            profit['buy'] / 1000).date()
        sell_date = datetime.datetime.utcfromtimestamp(
            profit['sell'] / 1000).date()
        
        return (f"Buy {args.currency.title()} on {buy_date} and sell on {sell_date} to maximize profits.")
    else:
        
        return (f"You shouldn't buy or sell {args.currency.title()} on the selected time period.")

    api.add_resource(main, '/args', endpoint='args')

    #This error handler is necessary for usage with Flask-RESTful.
    @parser.error_handler
    def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
        abort(error_status_code, errors=err.messages)



    def get_history_data():
    #get
        return history

    def check_prizes():
    #get
        return prize

    def days_sell():
    #post
        return days_sell

    def days_buy():
    #post
        return days_buy

@app.route('/', methods=['GET'])
def make_request():
    "if lauseet perustuen metodeihin"
    "joiden jälkeen requestin ajo"
    #create a datetime data object
    #cast `datetime_timestamp` as Timestamp object and compare
    #datetime_timestamp = tuple
    #datetime_timestamp = datetime_timestamp[args.date_from,args.date_from]
    #times = datetime.strptime(str(args.date_from), '%Y-%d-%m')
    l = False
    # check if time range is more than 90 days
    if args.date_to - args.date_from < timedelta(days=90):
        l = True
        # The API returns daily data (00:00 UTC) if time range is above 90 days
        extended = args.date_to + timedelta(days=90)

    try:
       
        url = f'https://api.coingecko.com/api/v3/coins/{args.currency.lower()}/market_chart/range?vs_currency=eur&from={args.date_from.timestamp()}&to={extended.timestamp() if l else args.date_to.timestamp()}'
        r = requests.get(url)
        data = json.loads(r.text)
    except requests.exceptions.RequestException as ex:
        raise SystemExit(ex)

    try:  # Only relevant values from the data
        if l:
            end = (extended-args.date_from).days - 90 + 1
            prices = data['prices'][0:end]
            volumes = data['total_volumes'][0:end]
        else:
            prices = data['prices']
            volumes = data['total_volumes']
    except KeyError:
        return('There is no prices available for that currency.')
        exit()

    trend = downward_trend(prices) #Get the maximum downward trend

    return(f"{args.currency.title()}'s price decreased {trend} days in a row for the selected time range.")

    timestamp, max_volume = trading_volume(volumes) # Get highest trading volume
    volume_date = datetime.utcfromtimestamp(timestamp / 1000).date() # Convert UNIX timestamp to a date

    return(f"{args.currency.title()}'s highest trading volume was {round(max_volume, 2)}€ on {volume_date}.")
   


    profit = best_profit(prices) # Get most profitable days and prices
    if profit is not None:
        buy_date = datetime.utcfromtimestamp(
            profit['buy'] / 1000).date()
        sell_date = datetime.utcfromtimestamp(
            profit['sell'] / 1000).date()
        return(
            f"Buy {args.currency.title()} on {buy_date} and sell on {sell_date} to maximize profits.")
    else:
        return(
            f"You shouldn't buy or sell {args.currency.title()} on the selected time period.")

    

    



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description="Dates are accepted in ISO 8601 format. (YYYY-DD-MM)")
    parser.add_argument('date_from', type=datetime.fromisoformat,
                        help="Start date of the time period.")
    parser.add_argument('date_to', type=datetime.fromisoformat,
                        help="End date of the time period.")
    parser.add_argument('--currency', nargs="?", type=str,
                        help="The cryptocurrency used in the calculations. Default is Bitcoin", default="bitcoin")
    args = parser.parse_args()
    
app.run(debug=True)
