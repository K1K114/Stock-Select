import yahoo_fin.stock_info as si
import pandas as pd
# "get_data provides open price, high, low, close, adjclose prices, volume and ticker"
#aapl = si.get_data('amzn', start_date='08/19/2024', end_date='08/23/2024')
#print((aapl))


# "code here provides just todays high"
#quote_table = si.get_data('AAPL', start_date="08/20/2024", end_date="08/24/2024")
#high = quote_table['high'].iloc[-1]
#print(f"{high:.2f}")
    # Moving Averages Comparison
        with alive_bar(len(self.stockslist), title="Processing Moving Averages", bar="smooth") as bar:
            for stock in self.stockslist:
                try:
                    fifty_day = si.get_stats(stock)["Value"][27]
                    twohundred_day = si.get_stats(stock)["Value"][28]
                    live_price = si.get_live_price(stock)
                    if live_price > fifty_day and live_price > twohundred_day:
                        scoring_chart_stocks[stock] += 5
                    elif live_price >= fifty_day and live_price <= twohundred_day:
                        scoring_chart_stocks[stock] += 4
                    elif live_price < fifty_day and live_price > twohundred_day:
                        scoring_chart_stocks[stock] += 3
                    elif live_price < fifty_day and live_price < twohundred_day and (1.05 * live_price) >= fifty_day or (1.05 * live_price) >= twohundred_day:
                        scoring_chart_stocks[stock] += 2
                    else:
                        scoring_chart_stocks[stock] += 1

                except Exception:
                    scoring_chart_stocks[stock] += 0
                bar()

# BETA Comparison
        with alive_bar(len(self.stockslist), title="Processing Beta", bar="smooth") as bar:
            for stock in self.stockslist:
                try:
                    stock_beta = si.get_quote_table(stock)["Beta (5Y Monthly)"]
                    if stock_beta > 1.5:
                        scoring_chart_stocks[stock] += 5
                    elif 1.0 < stock_beta <= 1.5:
                        scoring_chart_stocks[stock] += 4
                    elif 0.5 < stock_beta <= 1.0:
                        scoring_chart_stocks[stock] += 3
                    elif stock_beta <= 0.5:
                        scoring_chart_stocks[stock] += 1
                    else:
                        scoring_chart_stocks[stock] += 0
                except Exception:
                    scoring_chart_stocks[stock] += 0
                bar()
                
# RSI Calculator
        with alive_bar(len(self.stockslist), title="Processing RSI", bar="smooth") as bar:
            for stock in self.stockslist:
                try:
                    stock_data = si.get_data(stock, start_date="08/04/24", end_date="08/25/24")
                    only_adjclose_data = stock_data["adjclose"]
                    adj_close_value_list = []
                    for value in only_adjclose_data:
                        adj_close_value_list.append(value)

                    gains = 0
                    losses = 0

                    for index in range(len(adj_close_value_list)):
                        if index == 0:
                            None
                        else:
                            first_number = adj_close_value_list[index]
                            second_number = adj_close_value_list[index-1]

                            difference = first_number - second_number

                            if difference > 0:
                                gains += difference
                            elif difference < 0:
                                losses += difference*-1
                            else:
                                None


                    average_gain = gains/(len(adj_close_value_list)-1)

                    average_loss =  losses/(len(adj_close_value_list)-1)

                    if average_loss == 0:
                        RSI = 100
                    else:
                        RS = average_gain/average_loss

                        RSI = 100-(100/(1+RS))

                        if RSI > 70:
                            scoring_chart_stocks[stock] += 2
                        elif 50 < RSI <= 70:
                            scoring_chart_stocks[stock] += 4
                        elif 30 < RSI <= 50:
                            scoring_chart_stocks[stock] += 5
                        elif RSI <= 30:
                            scoring_chart_stocks[stock] += 3
                except Exception:
                    scoring_chart_stocks[stock] += 0
                bar()

# Volume Comparison
        volume_to_marketcap_ratio_ranking = {}
        sorted_volume_to_marketcap_ratio_ranking = {}
        with alive_bar(len(self.stockslist), title="Processing Volume", bar="smooth") as bar:
            for stock in self.stockslist:
                try:
                    stock_volume = si.get_quote_table(stock)["Volume"]
                    stock_marketcap = si.get_quote_table(stock)["Market Cap (intraday)"]

                    if isinstance(stock_marketcap, str):
                        if "T" in stock_marketcap:
                            stock_marketcap = float(stock_marketcap.replace("T", "")) * 1000000000000
                        elif "B" in stock_marketcap:
                            stock_marketcap = float(stock_marketcap.replace("B", "")) * 1000000000
                        elif "M" in stock_marketcap:
                            stock_marketcap = float(stock_marketcap.replace("M", "")) * 1000000

                    stock_volume_to_marketcap_ratio = stock_volume / stock_marketcap
                    volume_to_marketcap_ratio_ranking[stock] = stock_volume_to_marketcap_ratio

                except Exception:
                    continue
                bar()

            for key in sorted(volume_to_marketcap_ratio_ranking, key=volume_to_marketcap_ratio_ranking.get, reverse=True):
                sorted_volume_to_marketcap_ratio_ranking[key] = volume_to_marketcap_ratio_ranking[key]
                stock_name = list(sorted_volume_to_marketcap_ratio_ranking)[index]
                if index == 0:
                    scoring_chart_stocks[stock_name] += 5
                elif index == 1:
                    scoring_chart_stocks[stock_name] += 4
                elif index == 2:
                    scoring_chart_stocks[stock_name] += 3
                elif index == 3:
                    scoring_chart_stocks[stock_name] += 2
                elif index == 4:
                    scoring_chart_stocks[stock_name] += 1
                else:
                    scoring_chart_stocks[stock_name] += 0


