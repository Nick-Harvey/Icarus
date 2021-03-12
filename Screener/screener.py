import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

snp500 = pd.read_csv("core/s-and-p-500-companies-financials/data/constituents_csv.csv")
symbols = snp500['Symbol'].sort_values().tolist()

## Create the Dropdown menu
ticker = st.sidebar.selectbox(
	'Choose a S&P 500 Stock',
	symbols)

# Set the analysis type
infoType = st.sidebar.radio(
	"Choose an infoType",
	('Fundamental', 'Technical')

	)

# Display company information
if(infoType == 'Fundamental'):
	stock = yf.Ticker(ticker)
	info = stock.info
	st.title('Company Profile')
	st.subheader(info['longName'])
	st.markdown('** Sector **: ' + info['sector'])
	st.markdown('** Industry **: ' + info['industry'])
	st.markdown('** Phone **: ' + info['phone'])
	st.markdown('** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['country'])
	st.markdown('** Business Summary **')
	st.info(info['longBusinessSummary'])

	fundInfo = {
		'Enterprise Value (USD)': info['enterpriseValue'],
		'Enterprise To Revenue Ratio': info['enterpriseToRevenue'],
		'Enterprise To Ebitda Ratio': info['enterpriseToEbitda'],
		'Net Income (USD)': info['netIncomeToCommon'],
		'Profit Margin Ratio': info['profitMargins'],
		'Forward PE Ratio': info['forwardPE'],
		'PEG Ratio': info['pegRatio'],
		'Price to Book Ratio': info['priceToBook'],
		'Forward EPS (USD)': info['forwardEps'],
		'Beta ': info['beta'],
		'Book Value (USD)': info['bookValue'],
		'Dividend Rate (%)': info['dividendRate'],
		'Dividend Yield (%)': info['dividendYield'],
		'Five year Avg Dividend Yield (%)': info['fiveYearAvgDividendYield'],
		'Payout Ratio': info['payoutRatio']
	}

	fundDF = pd.DataFrame.from_dict(fundInfo, orient='index')
	fundDF = fundDF.rename(columns={0: 'Value'})
	st.subheader('Fundamental Info')
	st.table(fundDF)

	# Graph out stock price
	st.subheader('General Stock Info')
	st.markdown('** Market **: ' + info['market'])
	st.markdown('** Exchange **: ' + info['exchange'])
	st.markdown('** Quote Type **' + info['quoteType'])

	start = dt.datetime.today()-dt.timedelta(2 * 365)
	end = dt.datetime.today()
	df = yf.download(ticker, start, end)
	df = df.reset_index()
	fig = go.Figure(
		data=go.Scatter(x=df['Date'], y=df['Adj Close'])
		)

	fig.update_layout(
		title ={
			'text': "Stock Prices Over Past Two Years",
			'y':0.9,
			'x':0.5,
			'xanchor': 'center',
			'yanchor': 'top'})
	st.plotly_chart(fig, use_container_width=True)


	marketInfo = {
		"Volume": info['volume'],
		"Average Volume": info['averageVolume'],
		"Market Cap": info['marketCap'],
		"Float Shares": info['floatShares'],
		"Regular Market Price (USD)": info['regularMarketPrice'],
		"Bid Size": info['bidSize'],
		"Ask Size": info['askSize'],
		"Share Short": info['sharesShort'],
		"Short Ratio": info['shortRatio'],
		"Share Outstanding": info['sharesOutstanding']
	}

	marketDF = pd.DataFrame(data=marketInfo, index=[0])
	st.table(marketDF)
else:
	def calcMovingAverage(data, size):
		df = data.copy()
		df['sma'] = df['Adj Close'].rolling(size).mean()
		df['ema'] = df['Adj Close'].ewm(span=size, min_periods=size).mean()
		df.dropna(inplace=True)
		return df
	
	def calc_macd(data):
		df = data.copy()
		df['ema12'] = df['Adj Close'].ewm(span=12, min_periods=12).mean()
		df['ema26'] = df['Adj Close'].ewm(span=26, min_periods=26).mean()
		df['macd'] = df['ema12'] - df['ema26']
		df['signal'] = df['macd'].ewm(span=9, min_periods=9).mean()
		df.dropna(inplace=True)
		return df

	def calcBollinger(data, size):
		df = data.copy()
		df["sma"] = df['Adj Close'].rolling(size).mean()
		df["bolu"] = df["sma"] + 2*df['Adj Close'].rolling(size).std(ddof=0) 
		df["bold"] = df["sma"] - 2*df['Adj Close'].rolling(size).std(ddof=0) 
		df["width"] = df["bolu"] - df["bold"]
		df.dropna(inplace=True)
		return df

	st.title('Technical Analysis')
	st.subheader('Moving Average')

	coMA1, coMA2 = st.beta_columns(2)

	with coMA1:
		numYearMA = st.number_input('Insert period (Year): ', min_value=1, max_value=10, value=2, key=0)

	with coMA2:
		windowSizeMA = st.number_input('window Size (Day): ', min_value=5, max_value=500, value=20, key=1)

	# Calculate moving day average and get historical data
	start = dt.datetime.today()-dt.timedelta(numYearMA * 365)
	end = dt.datetime.today()
	dataMA = yf.download(ticker,start,end)

	# take stock data and window size as params and return moving average
	df_ma = calcMovingAverage(dataMA, windowSizeMA)
	df_ma = df_ma.reset_index()

	# Graph Moving day average
	figMA = go.Figure()

	figMA.add_trace(
		go.Scatter(
			x = df_ma['Date'],
			y = df_ma['Adj Close'],
			name = "Prices Over Last " + str(numYearMA) + " Year(s)"
			)
		)

	figMA.add_trace(
		go.Scatter(
			x = df_ma['Date'],
			y = df_ma['sma'],
			name = "EMA" + str(windowSizeMA) + " Over Last " + str(numYearMA) + " Year(s)"
			)
		)

	figMA.add_trace(
		go.Scatter(
			x = df_ma['Date'],
			y = df_ma['ema'],
			name = "EMA" + str(windowSizeMA) + " OVer Last " + str(numYearMA) + " Year(s)"
			)
		)

	figMA.update_layout(legend=dict(
		yanchor="top",
		y=0.99,
		xanchor="left",
		x=0.01
		))

	figMA.update_layout(legend_title_text='Trend')
	figMA.update_yaxes(tickprefix="$")

	st.plotly_chart(figMA, use_container_width=True)