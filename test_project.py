from project import get_alldata, get_industry_data, match_industry, short_term_invest, long_term_invest, rank_stocks, StockData, IndustryData, StockRecommendations


def test_get_alldata():
    stock_data = get_alldata("aapl")
    assert stock_data.liveprice != None
    assert stock_data.previouscloseprice != None
    assert stock_data.openingprice != None
    invalid_data = get_alldata("INVALID")
    assert invalid_data == None

def test_get_industry_data():
    data = get_industry_data("technology")
    assert data.industryname == "Top Technology Stocks' Data"
    assert len(data.stocklistdata) > 0

def test_match_industry():
    finance_stocks = match_industry("finance")
    assert isinstance(finance_stocks, list)
    assert len(finance_stocks) > 0

    invalid_stocks = match_industry("Inavlid")
    assert invalid_stocks == None

def test_short_term_invest():
    stocks = ["aapl", "msft"]
    scores = short_term_invest(stocks)
    assert isinstance(scores, dict)
    assert len(scores) == len(stocks)

def test_long_term_invest():
    stocks = ["aapl", "msft"]
    scores = long_term_invest(stocks)
    assert isinstance(scores, dict)
    assert len(scores) == len(stocks)

def rank_stocks():
    test_scores = {"aapl": 10, "msft": 12, "googl": 8}
    invest_goal = "short"
    recommendations = rank_stocks(test_scores, invest_goal)
    assert recommendations.first == "MSFT"
    assert recommendations.second == "AAPL"
    assert recommendations.third == "GOOGL"
