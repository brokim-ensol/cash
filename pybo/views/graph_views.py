from flask import Blueprint, render_template, request
from pybo.models import Balance, Repayment
import plotly
import plotly.express as px
import pandas as pd

bp = Blueprint('show', __name__, url_prefix='/show')

@bp.route('/')
def show_graph():
    return render_template('show.html')

@bp.route('/graph')
def graph():
    return gm()

def gm():
    # st = yf.Ticker(stock)

    # Create a line graph
    # df = st.history(period=(period), interval=interval)
    balance_list = Balance.query.all()
    #unpacking balance_list which is a list of Balance objects
    balance_data = [(balance.created_at, balance.ratio) for balance in balance_list]

    df = pd.DataFrame.from_records(balance_data, columns=["created_at", "ratio"])
    df['balance_ratio'] = 1 - df['ratio']
    #generate dataframe from the query

    fig = px.line(df, x="created_at", y="balance_ratio", title="ratio Graph")

    # Create a JSON representation of the graph
    graphJSON = fig.to_json()
    return graphJSON