from pyfiglet import Figlet
from tabulate import tabulate
import requests
import yahoo_fin.stock_info as si
from datetime import date
import re
import warnings
from alive_progress import alive_bar
import plotly.graph_objects as p
import os
import pandas as pd


warnings.filterwarnings("ignore")



class StockRecommendations():
    def __init__(self, invest_goal, industry_preferance):
        self.invest_goal = invest_goal
        self.industry_preferance = industry_preferance

    def match_industry(self):
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url)
        sp500_df = tables[0]
        dow_tickers = si.tickers_dow()
        sp_tickers = si.tickers_sp500()

        with alive_bar((len(dow_tickers)+ (len(sp_tickers)-400)), title="Matching Industry", bar="smooth") as bar:
            match self.industry_preferance:

                case "technology":

                    self.stockslist = []

                    # Sort through tech companies in dow jones index
                    tickers_dow = si.tickers_dow(include_company_data = True)
                    for index in range(len(tickers_dow["Company"])):
                        if tickers_dow["Industry"][index] in ["Information technology", "Communication Services", "Conglomerate", "Semiconductor industry"]:
                            self.stockslist.append(tickers_dow["Symbol"][index])
                        bar()
                        
                    # Sort through tech companies in S&P index
                    tickers_sp500 = si.tickers_sp500(include_company_data = True)
                    for index in range(len(tickers_sp500["Security"])-400):
                        if tickers_sp500["GICS Sector"][index] in ["Information Technology", "Communication Services"]:
                            self.stockslist.append(sp500_df["Symbol"][index])
                        bar()

                case "healthcare":

                    self.stockslist = []

                    # Sort through tech companies in dow jones index
                    tickers_dow = si.tickers_dow(include_company_data = True)
                    for index in range(len(tickers_dow["Company"])):
                        if tickers_dow["Industry"][index] in ["Pharmaceutical industry", "Managed health care", "Biopharmaceutical"]:
                            self.stockslist.append(tickers_dow["Symbol"][index])
                        bar()
                    # Sort through tech companies in S&P index
                    tickers_sp500 = si.tickers_sp500(include_company_data = True)
                    for index in range(len(tickers_sp500["Security"])):
                        if tickers_sp500["GICS Sector"][index] in ["Health Care"]:
                            self.stockslist.append(sp500_df["Symbol"][index])
                        bar()

                case "energy":

                    self.stockslist = []

                    # Sort through tech companies in dow jones index
                    tickers_dow = si.tickers_dow(include_company_data = True)
                    for index in range(len(tickers_dow["Company"])):
                        if tickers_dow["Industry"][index] in ["Petroleum industry"]:
                            self.stockslist.append(tickers_dow["Symbol"][index])
                        bar()
                    # Sort through tech companies in S&P index
                    tickers_sp500 = si.tickers_sp500(include_company_data = True)
                    for index in range(len(tickers_sp500["Security"])):
                        if tickers_sp500["GICS Sector"][index] in ["Energy", "Utilities"]:
                            self.stockslist.append(sp500_df["Symbol"][index])
                        bar()
                case "consumer goods":

                    self.stockslist = []

                    # Sort through tech companies in dow jones index
                    tickers_dow = si.tickers_dow(include_company_data = True)
                    for index in range(len(tickers_dow["Company"])):
                        if tickers_dow["Industry"][index] in ["Retailing", "Food industry", "Fast-moving consumer goods", "Drink industry", "Broadcasting and entertainment"]:
                            self.stockslist.append(tickers_dow["Symbol"][index])
                        bar()
                    # Sort through tech companies in S&P index
                    tickers_sp500 = si.tickers_sp500(include_company_data = True)
                    for index in range(len(tickers_sp500["Security"])):
                        if tickers_sp500["GICS Sector"][index] in ["Consumer Discretionary", "Consumer Staples"]:
                            self.stockslist.append(sp500_df["Symbol"][index])
                        bar()



    def short_term_invest(self):
        scoring_chart_stocks = {}
        for stock in self.stockslist:
            scoring_chart_stocks[stock] = 0
        # Look at beta, volume, moving averages, RSI, and Earnings Date data to make reccomendations
        # Beta: Higher beta indicates stock is better suited for short term growth, stock volatility
        # Volume: High volume suggests strong momentum, confirming strength of movement
        # Moving Averages:
        # RSI:
        # Earnings Date:
        # sort by each data one by one, top 5 add aa score to each,

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



        # Scoring Results
        with alive_bar(len(self.stockslist), title="Ranking Stocks", bar="smooth") as bar:
            sorted_scoring_chart_stocks = sorted(scoring_chart_stocks.keys(), key=scoring_chart_stocks.get, reverse=True)
            bar()

            top_five_stocks = list(sorted_scoring_chart_stocks)
            bar()

            first = top_five_stocks[0]
            second = top_five_stocks[1]
            third = top_five_stocks[2]
            fourth = top_five_stocks[3]
            fifth = top_five_stocks[4]
            bar()

            map(str, first, second, third, fourth, fifth)
            bar()

            self.scoring_chart_stocks = scoring_chart_stocks
            self.first = first
            self.second = second
            self.third = third
            self.fourth = fourth
            self.fifth = fifth
            bar()

            # DATA FOR 1
            self.one_quote = si.get_quote_table(first, dict_result=False)
            self.one_live = si.get_live_price(first)
            self.one_pe = si.get_quote_table(first)['PE Ratio (TTM)']
            self.one_eps = si.get_quote_table(first)['EPS (TTM)']
            self.one_fiftytwoweek = si.get_quote_table(first)['52 Week Range']
            bar()

            # DATA FOR 2
            self.two_quote = si.get_quote_table(second, dict_result=False)
            self.two_live = si.get_live_price(second)
            self.two_pe = si.get_quote_table(second)['PE Ratio (TTM)']
            self.two_eps = si.get_quote_table(second)['EPS (TTM)']
            self.two_fiftytwoweek = si.get_quote_table(second)['52 Week Range']
            bar()

            # DATA FOR 3
            self.three_quote = si.get_quote_table(third, dict_result=False)
            self.three_live = si.get_live_price(third)
            self.three_pe = si.get_quote_table(third)['PE Ratio (TTM)']
            self.three_eps = si.get_quote_table(third)['EPS (TTM)']
            self.three_fiftytwoweek = si.get_quote_table(third)['52 Week Range']
            bar()

            # DATA FOR 4
            self.four_quote = si.get_quote_table(fourth, dict_result=False)
            self.four_live = si.get_live_price(fourth)
            self.four_pe = si.get_quote_table(fourth)['PE Ratio (TTM)']
            self.four_eps = si.get_quote_table(fourth)['EPS (TTM)']
            self.four_fiftytwoweek = si.get_quote_table(fourth)['52 Week Range']
            bar()

            # DATA FOR 5
            self.five_quote = si.get_quote_table(fifth, dict_result=False)
            self.five_live = si.get_live_price(fifth)
            self.five_pe = si.get_quote_table(fifth)['PE Ratio (TTM)']
            self.five_eps = si.get_quote_table(fifth)['EPS (TTM)']
            self.five_fiftytwoweek = si.get_quote_table(fifth)['52 Week Range']
            bar()

def expert_analyst_recommendation():
    print("\n-----------------------Expert Analyst Stock Recommendation Generator-----------------------")
    print("                        First we are going to need some information\n                        ")

    invest_goal = input("1) Goals: Short term gains or Long term growth?: ").lower().strip()

    while invest_goal not in ["short", "short term", "short term gains", "s", "long", "long term", "long term growth", "l"]:
        invest_goal = input("  Enter a valid goal:  ").lower().strip()

    print("\n----------------Industry List----------------")
    print("1: Technology \n2: Healthcare \n3: Energy \n4: Consumer Goods")
    print("---------------------------------------------")
    industry_preferance = input("3) Industry Preferance: What industry/sector do you have a preference in? ").lower().strip()
    while industry_preferance not in ["technology", "finance", "healthcare", "energy", "consumer goods", "industrial", "real estate"]:
        industry_preferance = input("  Enter a valid industry: ").lower().strip()


    recommendations = StockRecommendations(invest_goal, industry_preferance)
    recommendations.match_industry()
    recommendations.short_term_invest()



    print("\n")
    print("----------------------------Our Recommendations Based On Your Preferances----------------------------\n")
    print(f"\n\n{recommendations.scoring_chart_stocks}\n\n")
    print(f"1: {recommendations.first}")
    print(f"    Live Price: {recommendations.one_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.one_pe}")
    print(f"    EPS (TTM): {recommendations.one_eps}")
    print(f"    52 Week Range: {recommendations.one_fiftytwoweek}")

    print(f"\n2: {recommendations.second}")
    print(f"    Live Price: {recommendations.two_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.two_pe}")
    print(f"    EPS (TTM): {recommendations.two_eps}")
    print(f"    52 Week Range: {recommendations.two_fiftytwoweek}")

    print(f"\n3: {recommendations.third}")
    print(f"    Live Price: {recommendations.three_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.three_pe}")
    print(f"    EPS (TTM): {recommendations.three_eps}")
    print(f"    52 Week Range: {recommendations.three_fiftytwoweek}")

    print(f"\n3: {recommendations.fourth}")
    print(f"    Live Price: {recommendations.four_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.four_pe}")
    print(f"    EPS (TTM): {recommendations.four_eps}")
    print(f"    52 Week Range: {recommendations.four_fiftytwoweek}")

    print(f"\n5: {recommendations.fifth}")
    print(f"    Live Price: {recommendations.five_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.five_pe}")
    print(f"    EPS (TTM): {recommendations.five_eps}")
    print(f"    52 Week Range: {recommendations.five_fiftytwoweek}")
    print("\n-----------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    expert_analyst_recommendation()

