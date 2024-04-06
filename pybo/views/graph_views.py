from flask import Blueprint, render_template, request, url_for
from pybo.models import Balance
import plotly.express as px
import pandas as pd
import os
from pathlib import Path

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
    balance_data = [(balance.repaid_dt, balance.ratio) for balance in balance_list]

    actual_df = pd.DataFrame.from_records(balance_data, columns=["created_at", "ratio"])
    actual_df['repayment_ratio'] = 1 - actual_df['ratio']
    actual_df['type'] = '실행'
    #sort the dataframe by created_at
    actual_df = actual_df.sort_values(by='created_at')
    #generate dataframe from the query
    this_file_path = Path(__file__)
    plan_df = pd.read_excel(this_file_path.parents[1].joinpath('static/simul.xlsx'))
    plan_df = plan_df[['created_at', 'repayment_ratio','type']]
    plan_df['created_at'] = pd.to_datetime(plan_df['created_at']).dt.date
    #concat the two dataframes
    df = pd.concat([actual_df, plan_df])

    fig = px.line(df, x="created_at", y="repayment_ratio", title="대출상환 진도율", markers=True, color='type', labels={'created_at': '월', 'repayment_ratio': '상환비율'}, range_x=[df['created_at'].min(), df['created_at'].max()])

    # Create a JSON representation of the graph
    graphJSON = fig.to_json()
    return graphJSON