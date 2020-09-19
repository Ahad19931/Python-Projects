from flask import Flask, render_template, request
from datetime import datetime
import requests
import pandas

app = Flask(__name__)

data = pandas.read_csv("NASDAQ.txt")
data = data.drop(data.columns[2:],1)

def get_company_name(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


@app.route('/plot', methods = ['POST'])
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.io import output_notebook
    from bokeh.resources import CDN
    from bokeh.models import HoverTool, ColumnDataSource

    def check_stock_val(close, open):
        if close > open:
            return "Increase"
        elif close < open:
            return "Decrease"
        else:
            return "Equal"
    
    if request.method == 'POST':
        stock = request.form["stock_name"]      
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        start_date_obj = datetime.datetime.strptime((start_date + " 00:00:00"), '%Y-%m-%d %H:%M:%S')
        end_date_obj = datetime.datetime.strptime((end_date + " 00:00:00"), '%Y-%m-%d %H:%M:%S')        
        company = get_company_name(stock)

        try:
            df = data.DataReader(name = stock , data_source = "yahoo", start = start_date_obj, end = end_date_obj) 

            df["Status"] = [check_stock_val(close, open) for close, open in zip(df.Close, df.Open)]
            df["Average"] = (df.Open + df.Close)/2
            df["Height"] = abs(df.Open-df.Close)
            
            df["IndexColumn"] = df.index
            df["IncreaseXaxis"] = pandas.Series(df.IndexColumn[df.Status == "Increase"])
            df["IncreaseYaxis"] = pandas.Series(df.Average[df.Status == "Increase"])
            df["IncreaseHeight"] = pandas.Series(df.Height[df.Status == "Increase"])
            df["DecreaseXaxis"] = pandas.Series(df.IndexColumn[df.Status == "Decrease"])
            df["DecreaseYaxis"] = pandas.Series(df.Average[df.Status == "Decrease"])
            df["DecreaseHeight"] = pandas.Series(df.Height[df.Status == "Decrease"])

            df["High_string"] = df["High"].astype(str)
            df["Low_string"] = df["Low"].astype(str)
            df["Open_string"] = df["Open"].astype(str)
            df["Close_string"] = df["Close"].astype(str)
            df["Date_string"] = df["IndexColumn"].astype(str)

            cds = ColumnDataSource(df)

            hours_12 = 12*60*60*1000
            fig = figure(x_axis_type = "datetime", width = 1000, height = 300, sizing_mode = "scale_width")
            fig.title.text = "Candle Stick Chart"
            fig.title.text_font_style = "bold"
            fig.title.text_font_size = '20pt'
            fig.grid.grid_line_alpha = 0.2

            hover = HoverTool(tooltips = [("Highest ","@High_string{1.11}"),("Lowest ","@Low_string{1.11}"),("Opened ","@Open_string{1.11}"),("Closed ","@Close_string{1.11}"),("Date ","@Date_string")])
            fig.add_tools(hover)

            fig.segment(x0 = "IndexColumn", y0 = "High", x1 = "IndexColumn", y1 = "Low", color = "Black", source = cds)
            fig.rect(x = "IncreaseXaxis", y = "IncreaseYaxis",
                    width = hours_12, height = "IncreaseHeight", fill_color = "#00ffbf", line_color = "black", source = cds)
            fig.rect(x = "DecreaseXaxis", y = "DecreaseYaxis",
                    width = hours_12, height = "DecreaseHeight", fill_color = "#cc0000", line_color = "black", source = cds)
            
            script1, div1 = components(fig)
            cdn_js = CDN.js_files[0]
            return render_template("plot.html", text1 = ("Company: " + company),  text2 = ("Start Date: " + start_date), text3 = ("End Date: " + end_date),
            script1 = script1, div1 = div1, cdn_js = cdn_js)
        except:
            return render_template("home.html", text = "The stock symbol entered does not exist. Please check again!")


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/list-of-stocks/')
def list_of_stocks():
    return render_template("list_of_stocks.html", text = data.to_html())

@app.route('/description/')
def description():
    return render_template("description.html")

if __name__ == "__main__":
    app.run(debug = True)