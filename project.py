# ALL LIBRARIES
from pyfiglet import Figlet
from tabulate import tabulate
import yahoo_fin.stock_info as si
from datetime import date, timedelta
import warnings
from alive_progress import alive_bar
import plotly.graph_objects as p
import os
import pandas as pd

# My project is going to be a stock market data retriever.
# Where users can filter what stocks they want to see or if they want to search up specfically one stock.
# Depending on the input, the program will print out the current value in USD of the stock(s) and then if user wants, program will showcase a graph of the year to date stock fund price



os.system('clear')
warnings.filterwarnings("ignore")

class StockData():
    def __init__(self, stock, data, quotetable, liveprice, previouscloseprice, openingprice, highprice, lowprice, fiftytworange, marketcap, volume, avgvolume, peratio, yeartarget, pastyeardata, chart):
        self.stock = stock
        self.data = data
        self.quotetable = quotetable
        self.liveprice = liveprice
        self.previouscloseprice = previouscloseprice
        self.openingprice = openingprice
        self.highprice = highprice
        self.lowprice = lowprice
        self.fiftytworange = fiftytworange
        self.marketcap = marketcap
        self.volume = volume
        self.avgvolume = avgvolume
        self.peratio = peratio
        self.yeartarget = yeartarget
        self.pastyeardata = pastyeardata
        self.chart = chart


class IndustryData():
    def __init__(self, industryname, stocklistdata, stocklistdataheaders):
        self.industryname = industryname
        self.stocklistdata = stocklistdata
        self.stocklistdataheaders = stocklistdataheaders


class StockRecommendations():
    def __init__(self, first, one_des, one_live, one_pe, one_eps, one_fiftytwoweek, one_data, firstyesorno, first_percent_change, second, two_des, two_live, two_pe, two_eps, two_fiftytwoweek, two_data, secondyesorno, second_percent_change, third, three_des, three_live, three_pe, three_eps, three_fiftytwoweek, three_data, thirdyesorno, third_percent_change):
        # First
        self.first = first
        self.one_des = one_des
        self.one_live = one_live
        self.one_pe = one_pe
        self.one_eps = one_eps
        self.one_fiftytwoweek = one_fiftytwoweek
        self.one_data = one_data
        self.firstyesorno = firstyesorno
        self.first_percent_change = first_percent_change

        # Second
        self.second = second
        self.two_des = two_des
        self.two_live = two_live
        self.two_pe = two_pe
        self.two_eps = two_eps
        self.two_fiftytwoweek = two_fiftytwoweek
        self.two_data = two_data
        self.secondyesorno = secondyesorno
        self.second_percent_change = second_percent_change

        # Third
        self.third = third
        self.three_des = three_des
        self.three_live = three_live
        self.three_pe = three_pe
        self.three_eps = three_eps
        self.three_fiftytwoweek = three_fiftytwoweek
        self.three_data = three_data
        self.thirdyesorno = thirdyesorno
        self.third_percent_change = third_percent_change





def main():
    while True:
        display()
        matching_user_input()

        a = input("\nGo back (y/n)? ")
        if a in ["yes", "y"]:
            None
        else:
            break

    ending_text = "Ending Session..."
    font = Figlet(font="larry3d")
    print(font.renderText(ending_text))



def display():
    display_text = "Welcome to Stock Select"
    font = Figlet(font="larry3d")
    print(font.renderText(display_text))

    # Use tabulate to present the filters in a table format with headers,
    table = [[1, "Search a Stock"],[2, "Industry/Sector"], [3, "Expert Analyst Recommendations"] ]
    headers = ["ID", "Filters"]
    print(tabulate(table, headers, tablefmt="outline"))
    print("")



def matching_user_input():
    ID = input("Enter any ID: ").strip()

    while ID not in ["1", "2", "3", "4"]:
        ID = input("Please enter a valid ID: ")

    match ID:
        case "1":
            specfic_stock_selector()
        case "2":
            industry_sector_filter()
        case "3":
            expert_analyst_recommendation()


def specfic_stock_selector():
    print("\n---------------------Choose Stock---------------------")
    stock = input("\nEnter the Stock/Index Ticker: ").strip().upper()
    print("")
    while True:
        try:
            si.get_live_price(stock)
            break
        except AssertionError:
            stock = input("No data available for given stock ticker...\nEnter Valid Stock/Index Ticker: ").strip().upper()

    # Below is a work in process
    #startdate = input("Enter the Start Date for the Data: ")
    #enddate = input("Enter the End Date for the Data: ")

    alldata = get_alldata(stock)

    print(f"\n-----------{alldata.stock}'s Market Data Today (USD)-----------\n")
    print(f"Current Price: {alldata.liveprice:.2f}")
    print(f"Previous Day Closing Price: {alldata.previouscloseprice}")
    print(f"Opening Price: {alldata.openingprice:.2f}")
    print(f"Day's Range: {alldata.lowprice:.2f}-{alldata.highprice:.2f}")
    print(f"52 Week Range: {alldata.fiftytworange}")
    print(f"Market Cap: {alldata.marketcap}")
    print(f"Stock Volume: {alldata.volume}")
    print(f"Avg Volume: {alldata.avgvolume}")
    print(f"PE Ratio (TTM): {alldata.peratio}")
    print(f"1y Target Est: {alldata.yeartarget}\n")
    print("----------------------------------------------------\n")

    historicaldata = input(f"Would you like {stock}'s past year Historical Data (y/n): ")
    if historicaldata.lower() == "yes" or historicaldata.lower() == "y":
        print("\nHistorical Data:")
        dataheaders = ["Date", "Open(USD)", "High(USD)", "Low(USD)", "Close(USD)", "Adjclose(USD)", "Volume", "Company"]
        print(tabulate(alldata.data, dataheaders, tablefmt='grid'))

    graph = input(f"\nWould you like {stock}'s past year Stock Chart (y/n)? ")
    if graph.lower() in ["y", "yes"]:
        alldata.chart.show()

    else:
        print("\nExiting Data View")



def get_alldata(stock):
        try:
            with alive_bar(3, title="Retrieving Data", bar="smooth") as bar:
                # GET DATE DATA
                today_date = (date.today())
                new_date = today_date - timedelta(weeks=52)

                year, month, day = str(today_date).split("-")
                newyear, newmonth, newday = str(new_date).split("-")

                end_date = f"{month}/{day}/{year}"
                start_date = f"{newmonth}/{newday}/{newyear}"


                # GET STOCK DATA
                data = si.get_data(stock, start_date=start_date, end_date=end_date, interval="1mo")
                bar(0.33)
                quotetable = si.get_quote_table(stock)
                bar(0.67)
                # GET LIVE PRICE
                liveprice = si.get_live_price(stock)
                # GET PREVIOUS DAY CLOSE PRICE
                previouscloseprice = quotetable["Previous Close"]
                # GET OPENING PRICE
                openingprice = data['open'].iloc[-1]
                # GET HIGH AND LOW PRICE
                highprice = data['high'].iloc[-1]
                lowprice = data['low'].iloc[-1]
                # GET 52 WEEK RANGE (highest and lowest prices over psat 52 weeks)
                fiftytworange = quotetable["52 Week Range"]
                # GET MARKET CAP
                try:
                    marketcap = quotetable["Market Cap (intraday)"]
                except KeyError:
                    marketcap = "None"
                # GET VOLUME
                volume = data['volume'].iloc[-1]
                # GET AVG. VOLUME
                avgvolume = quotetable["Avg. Volume"]
                # GET PE RATIO (TTM)
                try:
                    peratio = quotetable["PE Ratio (TTM)"]
                    # GET 1Y TARGET EST
                    yeartarget = quotetable["1y Target Est"]
                except KeyError:
                    peratio = "None"
                    yeartarget = "None"
                # GET PAST YEAR GRAPH
                pastyeardata = si.get_data(stock, start_date=start_date, end_date=end_date, interval="1d")
                bar(1.)
                chart = p.Figure(data=p.Scatter(x=pastyeardata.index, y=pastyeardata["close"], mode="lines+markers"))
                # SET and RETURN ALL DATA TO A CLASS
                all_data = StockData(stock, data, quotetable, liveprice, previouscloseprice, openingprice, highprice, lowprice, fiftytworange, marketcap, volume, avgvolume, peratio, yeartarget, pastyeardata, chart)

                return all_data

        except AssertionError:
            print("No data available for given stock ticker")




def industry_sector_filter():
    print("---------------------Industry List---------------------")
    print("1: Technology \n2: Finance \n3: Healthcare \n4: Energy \n5: Consumer Goods \n6: Industrial \n7: Real Estate")
    print("-------------------------------------------------------\n")
    industry = input("Enter Industry: ").lower()

    while industry not in ["technology", "finance", "healthcare", "energy", "consumer goods", "industrial", "real estate"]:
        print("Error: Invalid Industry")
        industry = input("Please enter a proper Industry: ")
        print('')

    industrydata = get_industry_data(industry)

    print(f"\n\n{industrydata.industryname}\n")
    print(tabulate(industrydata.stocklistdata, industrydata.stocklistdataheaders, tablefmt="grid"))

def get_industry_data(industry):
    match industry:
            case "technology":
                industryname = "Top Technology Stocks' Data"
                stockslist = ["Apple Inc. (AAPL)", "Microsoft Corporation (MSFT)", "Alphabet Inc. (GOOGL)", "Amazon.com, Inc. (AMZN)", "NVIDIA Corporation (NVDA)", "Meta Platforms, Inc. (META)", "Tesla, Inc. (TSLA)", "Intel Corporation (INTC)", "Cisco Systems, Inc. (CSCO)", "Adobe Inc. (ADBE)"]


            case "finance":
                industryname = "Top Finance Stocks' Data"
                stockslist = ["Berkshire Hathaway Inc. (BRK-B)", "JPMorgan Chase & Co. (JPM)", "Visa Inc. (V)", "Mastercard Incorporated (MA)", "Bank of America Corporation (BAC)", "Wells Fargo & Company (WFC)", "Goldman Sachs Group, Inc. (GS)", "Morgan Stanley (MS)", "American Express Company (AXP)", "Blackstone Inc. (BX)"]


            case "healthcare":
                industryname = "Top Healthcare Stocks' Data"
                stockslist = ["Eli Lily and Co. (LLY)", "UnitedHealth Group Inc. (UNH)", "Johnson & Johnson (JNJ)", "AbbVie Inc. (ABBV)", "Merck & Co., Inc. (MRK)", "Thermo Fisher Scientific Inc. (TMO)", "Abbott Laboratories (ABT)", "Danaher Corporation (DHR)", "Amgen Inc. (AMGN)", "Intuitive Surgical, Inc. (ISRG)"]


            case "energy":
                industryname = "Top Energy Stocks' Data"
                stockslist = ["Texas Instruments Incorporated (TXN)", "Exxon Mobil Corporation (XOM)", "Chevron Corporation (CVX)", "ConocoPhillips (COP)", "EOG Resources, Inc. (EOG)", "Schlumberger Limited (SLB)", "Enterprise Products Partners L.P. (EPD)", "Marathon Petroleum Corporation (MPC)", "Phillips 66 (PSX)", "Energy Transfer LP (ET)"]


            case "consumer goods":
                industryname = "Top Consumer Good Stocks' Data"
                stockslist = ["Amazon.com, Inc. (AMZN)", "Tesla, Inc. (TSLA)", "The Home Depot, Inc. (HD)", "McDonald's Corporation (MCD)", "Lowe's Companies, Inc. (LOW)", "The TJX Companies, Inc. (TJX)", "Booking Holdings Inc. (BKNG)", "NIKE, Inc. (NKE)", "Starbucks Corporation (SBUX)", "MercadoLibre, Inc. (MELI)"]

            case "industrial":
                industryname = "Top Industrial Stocks'Data"
                stockslist = ["General Electric Company (GE)", "Caterpillar Inc. (CAT)", "RTX Corporation (RTX)", "Union Pacific Corporation (UNP)", "Lockheed Martin Corporation (LMT)", "Honeywell International Inc. (HON)", "Eaton Corporation plc (ETN)", "United Parcel Service, Inc. (UPS)", "The Boeing Company (BA)", "Deere & Company (DE)"]

            case "real estate":
                industryname = "Top Real Estate Stocks'Data"
                stockslist = ["Prologis, Inc. (PLD)", "American Tower Corporation (AMT)", "Equinix, Inc. (EQIX)", "Welltower Inc. (WELL)", "Simon Property Group, Inc. (SPG)", "Public Storage (PSA)", "Realty Income Corporation (O)", "Digital Realty Trust, Inc. (DLR)", "Crown Castle Inc. (CCI)", "Extra Space Storage Inc. (EXR)"]

    # Depending on Match, this retrieves the right sectors data
    stocklistdata = []
    stocklistdataheaders = ["Company", "Quote (USD)", "Open (USD)", "Close (USD)", "Day's Range (USD)", "52 Week Range (USD)", "PE Ratio (TTM)", "Volume", "1y Target Est (USD)"]

    with alive_bar(10, title="Retrieving Data", bar="smooth") as bar:
        for stock in stockslist:
            ticker = stock.split('(')[-1].strip(")")
            stockdata = si.get_quote_table(ticker)
            stockliveprice = si.get_live_price(ticker)
            data =  [stock, stockliveprice, stockdata['Open'], stockdata["Previous Close"], stockdata["Day's Range"], stockdata["52 Week Range"], stockdata["PE Ratio (TTM)"], stockdata["Volume"], stockdata["1y Target Est"]]
            stocklistdata.append(data)
            bar()

    return IndustryData(industryname, stocklistdata, stocklistdataheaders)

def expert_analyst_recommendation():
    print("\n-----------------------Expert Analyst Stock Recommendation Generator-----------------------")
    print("                        First we are going to need some information\n                        ")

    invest_goal = input("1) Goals: Short term gains or Long term growth?: ").lower().strip()
    while invest_goal not in ["short", "short term", "short term gains", "s", "long", "long term", "long term growth", "l"]:
        invest_goal = input("  Enter a valid goal:  ").lower().strip()

    print("\n----------------Industry List----------------")
    print("1: Technology \n2: Finance \n3: Healthcare \n4: Energy \n5: Consumer Goods \n6: Industrial \n7: Real Estate")
    print("---------------------------------------------")

    industry_preferance = input("2) Industry Preferance: What industry/sector do you have a preference in? ").lower().strip()
    while industry_preferance not in ["technology", "finance", "healthcare", "energy", "consumer goods", "industrial", "real estate"]:
        industry_preferance = input("  Enter a valid industry: ").lower().strip()

    stockslist = match_industry(industry_preferance)

    if invest_goal in ["short", "short term", "short term gains", "s"]:
        scoring_chart_stocks = short_term_invest(stockslist)

    elif invest_goal in ["long", "long term", "long term growth", "l"]:
        scoring_chart_stocks = long_term_invest(stockslist)

    recommendations = rank_stocks(scoring_chart_stocks, invest_goal)


    print("\n")
    print("----------------------------Our Recommendations Based On Your Preferances----------------------------\n")
    print(f"1: {recommendations.first}'s Stock {recommendations.one_des}")
    print(f"    Live Price: {recommendations.one_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.one_pe}")
    print(f"    EPS (TTM): {recommendations.one_eps}")
    print(f"    52 Week Range: {recommendations.one_fiftytwoweek}")
    if recommendations.firstyesorno:
        print(f"        **Note**: {recommendations.first} has gained {recommendations.first_percent_change:.2f}% in the last 2 weeks!")

    print(f"\n2: {recommendations.second}'s Stock {recommendations.two_des}")
    print(f"    Live Price: {recommendations.two_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.two_pe}")
    print(f"    EPS (TTM): {recommendations.two_eps}")
    print(f"    52 Week Range: {recommendations.two_fiftytwoweek}")
    if recommendations.secondyesorno:
        print(f"        **Note**: {recommendations.second} has gained {recommendations.second_percent_change:.2f}% in the last 2 weeks!")

    print(f"\n3: {recommendations.third}'s Stock {recommendations.three_des}")
    print(f"    Live Price: {recommendations.three_live:.2f}")
    print(f"    PE Ratio (TTM): {recommendations.three_pe}")
    print(f"    EPS (TTM): {recommendations.three_eps}")
    print(f"    52 Week Range: {recommendations.three_fiftytwoweek}")
    if recommendations.thirdyesorno:
        print(f"        **Note**: {recommendations.third} has gained {recommendations.third_percent_change:.2f}% in the last 2 weeks!")
    print("\n-----------------------------------------------------------------------------------------------------")


def match_industry(industry_preferance):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_df = tables[0]
    dow_tickers = si.tickers_dow()
    sp_tickers = si.tickers_sp500()

    with alive_bar((len(dow_tickers)+ (len(sp_tickers)-400)), title="Matching Industry", bar="smooth") as bar:
        match industry_preferance:
            case "technology":

                stockslist = []

                # Sort through tech companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Information technology", "Communication Services", "Conglomerate", "Semiconductor industry"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()
                # Sort through tech companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Information Technology", "Communication Services"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case "finance":

                stockslist = []

                # Sort through finance companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Financial services"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()
                # Sort through finance companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Financials"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case "healthcare":

                stockslist = []

                # Sort through healthcare companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Pharmaceutical industry", "Managed health care", "Biopharmaceutical"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()
                # Sort through healthcare companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Health Care"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case "energy":

                stockslist = []

                # Sort through energy companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Petroleum industry"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()
                # Sort through energy companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Energy", "Utilities"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case "consumer goods":

                stockslist = []

                # Sort through consumer goods companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Retailing", "Food industry", "Fast-moving consumer goods", "Drink industry", "Broadcasting and entertainment"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()
                # Sort through consumer goods companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Consumer Discretionary", "Consumer Staples"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case "industrial":

                stockslist = []

                # Sort through industrial companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Construction and mining", "Conglomerate", "Chemical industry"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()
                # Sort through industrial companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Industrials", "Materials"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case "real estate":
                stockslist = []

                # Sort through real estate companies in dow jones index
                tickers_dow = si.tickers_dow(include_company_data = True)
                for index in range(len(tickers_dow["Company"])):
                    if tickers_dow["Industry"][index] in ["Real Estate"]:
                        stockslist.append(tickers_dow["Symbol"][index])
                    bar()

                # Sort through real estate companies in S&P index
                tickers_sp500 = si.tickers_sp500(include_company_data = True)
                for index in range(len(tickers_sp500["Security"])-400):
                    if tickers_sp500["GICS Sector"][index] in ["Real Estate"]:
                        stockslist.append(sp500_df["Symbol"][index])
                    bar()

            case _:
                stockslist = None


    return stockslist


def short_term_invest(stockslist):
    # Look at beta, moving averages, and RSI data to make short term investing reccomendations
    # Beta: Higher beta indicates stock is better suited for short term growth, stock volatility
    # Moving Averages: Comparison between possible 200 day mark or 50 day mark
    # RSI: Relative Strenght Index, strong indicator of stocks short term investing potential
    # sort by each data one by one, top 5 add aa score to each

    scoring_chart_stocks = {}

    with alive_bar(len(stockslist), title="Processing Data", bar="smooth") as bar:
        for stock in stockslist:
            try:
                today_date = (date.today())
                new_date = today_date - timedelta(weeks=2)

                year, month, day = str(today_date).split("-")
                newyear, newmonth, newday = str(new_date).split("-")

                end_date = f"{month}/{day}/{year}"
                start_date = f"{newmonth}/{newday}/{newyear}"


                scoring_chart_stocks[stock] = 0
                stock_quote = si.get_quote_table(stock)
                stock_data = si.get_data(stock, start_date=start_date, end_date=end_date)

                try:
                    # BETA Comparison
                    stock_beta = stock_quote["Beta (5Y Monthly)"]
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


                try:
                    # Moving Averages Comparison
                    fifty_day = si.get_stats(stock)["Value"][27]
                    live_price = si.get_live_price(stock)
                    if live_price > fifty_day:
                        scoring_chart_stocks[stock] += 5
                    elif live_price >= fifty_day*0.95:
                        scoring_chart_stocks[stock] += 4
                    elif live_price < fifty_day:
                        scoring_chart_stocks[stock] += 3
                    else:
                        scoring_chart_stocks[stock] += 1

                except Exception:
                    scoring_chart_stocks[stock] += 0


                try:
                    # RSI Calculator
                    only_adjclose_data = stock_data["adjclose"]
                    adj_close_value_list = []
                    for value in only_adjclose_data:
                        adj_close_value_list.append(value)
                    gains = 0
                    losses = 0
                    for index in range(len(adj_close_value_list)):
                        if index == 0:
                            continue
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

            except Exception:
                continue

    return scoring_chart_stocks


def long_term_invest(stockslist):
    # Look at PE Ratio, EPS, Forward Dividend & yield, BETA 5Y Monthly data to make long term investing recommenations
    # PE Ratio:
    # EPS:
    # Forward Dividend & Yield:
    # BETA 5Y Monthly:
    # 52 Week Range:

    scoring_chart_stocks = {}

    with alive_bar(len(stockslist), title="Processing Data", bar="smooth") as bar:
        for stock in stockslist:
            try:
                scoring_chart_stocks[stock] = 0
                stock_data = si.get_quote_table(stock)

                try:
                    # PE Ratio Comparison
                    stock_peratio = stock_data["PE Ratio (TTM)"]

                    if 10 <= stock_peratio <= 20:
                        scoring_chart_stocks[stock] += 5
                    elif 20 < stock_peratio <= 25:
                        scoring_chart_stocks[stock] += 4
                    elif 5 <= stock_peratio < 10 or 25 < stock_peratio <= 30:
                        scoring_chart_stocks[stock] += 3
                    elif 30 < stock_peratio <= 40:
                        scoring_chart_stocks[stock] += 2
                    elif  stock_peratio < 5 or stock_peratio > 40:
                        scoring_chart_stocks[stock] += 1

                except Exception:
                    scoring_chart_stocks[stock] += 0


                try:
                    # EPS Comparison
                    stock_eps = stock_data["EPS (TTM)"]

                    if stock_eps > 10:
                        scoring_chart_stocks[stock] += 5
                    elif 5 <= stock_eps <= 10:
                        scoring_chart_stocks[stock] += 4
                    elif 1 <= stock_eps < 5:
                        scoring_chart_stocks[stock] += 3
                    elif 0 < stock_eps < 1:
                        scoring_chart_stocks[stock] += 2
                    elif stock_eps <= 0:
                        scoring_chart_stocks[stock] += 1

                except Exception:
                    scoring_chart_stocks[stock] += 0


                try:
                    # Forward Dividend & Yield Comparison
                    stock_dy = stock_data["Forward Dividend & Yield"]

                    unnecessary, percent = stock_dy.split()
                    percent = percent.replace("(", "")
                    percent = percent.replace(")", "")
                    percent = percent.replace("%", "")
                    percent = float(percent)

                    if 2 <= percent <= 4:
                        scoring_chart_stocks[stock] += 5
                    elif 4 < percent <= 5 or 1 <= percent <= 2:
                        scoring_chart_stocks[stock] += 4
                    elif percent > 5 or 0.5 <= percent < 1:
                        scoring_chart_stocks[stock] += 3
                    elif 0 <= percent < 0.5:
                        scoring_chart_stocks[stock] += 2
                    else:
                        scoring_chart_stocks[stock] += 1

                except Exception:
                    scoring_chart_stocks[stock] += 0


                try:
                    # BETA 5Y Monthly Comparison
                    stock_beta = stock_data["BETA (5Y Monthly)"]

                    if 0.8 <= stock_beta <= 1.2:
                        scoring_chart_stocks[stock] += 5
                    elif 0.5 <= stock_beta < 0.8 or 1.2 < stock_beta <= 1.5:
                        scoring_chart_stocks[stock] += 4
                    elif 0.3 <= stock_beta < 0.5 or 1.5 < stock_beta <= 2.0:
                        scoring_chart_stocks[stock] += 3
                    elif stock_beta < 0.3 or 2.0 < stock_beta <= 2.5:
                        scoring_chart_stocks[stock] += 2
                    elif 2.5 < stock_beta:
                        scoring_chart_stocks[stock] += 1

                except Exception:
                    scoring_chart_stocks[stock] += 0

                bar()

            except Exception:
                continue

    return scoring_chart_stocks


def rank_stocks(scoring_chart_stocks, invest_goal):
    # Scoring Results
    today_date = (date.today())
    new_date = today_date - timedelta(weeks=2)

    year, month, day = str(today_date).split("-")
    newyear, newmonth, newday = str(new_date).split("-")

    end_date = f"{month}/{day}/{year}"
    start_date = f"{newmonth}/{newday}/{newyear}"

    with alive_bar(3, title="Ranking Stocks", bar="smooth") as bar:
        sorted_scoring_chart_stocks = sorted(scoring_chart_stocks.keys(), key=scoring_chart_stocks.get, reverse=True)


        top_stocks = list(sorted_scoring_chart_stocks)


        first = top_stocks[0]
        second = top_stocks[1]
        third = top_stocks[2]



        map(str, first, second, third)

        # DATA FOR 1
        if invest_goal in ["short", "short term", "short term gains", "s"]:
            one_des = "- strongest contender for short-term gains with very solid momentum indicators"
        elif invest_goal in ["long", "long term", "long term growth", "l"]:
            one_des = "- strongest contender for long-term gains with very solid momentum indicators"

        one_live = si.get_live_price(first)
        one_pe = si.get_quote_table(first)['PE Ratio (TTM)']
        one_eps = si.get_quote_table(first)['EPS (TTM)']
        one_fiftytwoweek = si.get_quote_table(first)['52 Week Range']
        one_data = si.get_data(first, start_date=start_date, end_date=end_date)["close"]
        if one_data.iloc[-1]-one_data.iloc[0] > 0:
            firstyesorno = True
            first_percent_change = ((one_data.iloc[-1]-one_data.iloc[0])/one_data.iloc[0]) * 100
        else:
            first_percent_change = 0
            firstyesorno = False

        bar()

        # DATA FOR 2
        if invest_goal in ["short", "short term", "short term gains", "s"]:
            two_des = "- 2nd strongest contender for short-term gains with momentum variables still heavily indicating short term profits"
        elif invest_goal in ["long", "long term", "long term growth", "l"]:
            two_des = "- 2nd strongest contender for long-term gains with momentum variables still heavily indicating long term profits"

        two_live = si.get_live_price(second)
        two_pe = si.get_quote_table(second)['PE Ratio (TTM)']
        two_eps = si.get_quote_table(second)['EPS (TTM)']
        two_fiftytwoweek = si.get_quote_table(second)['52 Week Range']
        two_data = si.get_data(second, start_date=start_date, end_date=end_date)["close"]
        if two_data.iloc[-1]-two_data.iloc[0] > 0:
            secondyesorno = True
            second_percent_change = ((two_data.iloc[-1]-two_data.iloc[0])/two_data.iloc[0]) * 100
        else:
            second_percent_change = 0
            secondyesorno = False

        bar()

        # DATA FOR 3
        if invest_goal in ["short", "short term", "short term gains", "s"]:
            three_des = "- 3rd strongest contender for short-term gains with still strong momentum indicators leaning to short term profit"
        elif invest_goal in ["long", "long term", "long term growth", "l"]:
            three_des = "- 3rd strongest contender for long-term gains with still strong momentum indicators leaning to long term profit"

        three_live = si.get_live_price(third)
        three_pe = si.get_quote_table(third)['PE Ratio (TTM)']
        three_eps = si.get_quote_table(third)['EPS (TTM)']
        three_fiftytwoweek = si.get_quote_table(third)['52 Week Range']
        three_data = si.get_data(third, start_date=start_date, end_date=end_date)["close"]
        if three_data.iloc[-1]-three_data.iloc[0] > 0:
            thirdyesorno = True
            third_percent_change = ((three_data.iloc[-1]-three_data.iloc[0])/three_data.iloc[0]) * 100
        else:
            third_percent_change = 0
            thirdyesorno = False

        bar()

    return StockRecommendations(first, one_des, one_live, one_pe, one_eps, one_fiftytwoweek, one_data, firstyesorno, first_percent_change, second, two_des, two_live, two_pe, two_eps, two_fiftytwoweek, two_data, secondyesorno, second_percent_change, third, three_des, three_live, three_pe, three_eps, three_fiftytwoweek, three_data, thirdyesorno, third_percent_change)



if __name__ == "__main__":
    main()
