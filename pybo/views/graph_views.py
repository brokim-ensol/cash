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
    balance_list = Balance.query.all()
    balance_data = [(balance.repaid_dt, balance.ratio) for balance in balance_list]

    actual_df = pd.DataFrame.from_records(balance_data, columns=["created_at", "ratio"])
    actual_df['repayment_ratio'] = 1 - actual_df['ratio']
    actual_df['type'] = '실행'
    actual_df = actual_df.sort_values(by=['created_at','repayment_ratio'])
    actual_df = actual_df[['created_at', 'repayment_ratio','type']]
    actual_df['created_at'] = pd.to_datetime(actual_df['created_at']).dt.date
    ref_date = actual_df.tail(1)['created_at'].values[0]
    #generate dataframe from the query
    this_file_path = Path(__file__)    
    plan_df = pd.read_excel(this_file_path.parents[1].joinpath('static/simul.xlsx'))
    plan_df = plan_df[['created_at', 'repayment_ratio','type']]
    plan_df['created_at'] = pd.to_datetime(plan_df['created_at']).dt.date
    # plan_df['created_at'] 중에서 ref_date와 가장 가까운 날짜를 찾아서 반환
    # ref_date = datetime.datetime.strptime('2024-02-16', '%Y-%m-%d').date()
    bottom_dt = plan_df.loc[plan_df[plan_df.created_at <= ref_date].index.max(),'created_at']
    upper_dt = plan_df.loc[plan_df[plan_df.created_at >= ref_date].index.min(),'created_at']
    bottom_idx = plan_df[plan_df.created_at == bottom_dt].index.max()
    upper_idx = plan_df[plan_df.created_at == upper_dt].index.max()
    if bottom_idx != upper_idx:
        records = []
        records.append(plan_df.iloc[bottom_idx,:].to_dict())
        records.append({'created_at':ref_date, 'repayment_ratio':None, 'type':'계획'})
        records.append(plan_df.iloc[upper_idx,:].to_dict())
        interpolated_df = pd.DataFrame.from_records(records)
        interpolated_df['repayment_ratio'] = interpolated_df['repayment_ratio'].interpolate(method='linear')
        plan_repayment_ratio = interpolated_df.loc[interpolated_df['created_at'] == ref_date, 'repayment_ratio'].values[0]
    else:
        plan_repayment_ratio = plan_df.iloc[bottom_idx, :].repayment_ratio
        
    actual_repayment_ratio = actual_df.loc[actual_df['created_at'] == ref_date, 'repayment_ratio'].values[-1]
    diff_ratio = actual_repayment_ratio - plan_repayment_ratio
    # print(f'ref_date: {ref_date}, bottom_dt: {bottom_dt}, upper_dt: {upper_dt}, bottom_idx: {bottom_idx}, upper_idx: {upper_idx}')
    # print(f'actual_repayment_ratio: {actual_repayment_ratio}, plan_repayment_ratio: {plan_repayment_ratio}, diff_ratio: {diff_ratio}')
    annontated_text = f'계획 대비 차이: {diff_ratio*100:.1f} (%), {32000*diff_ratio:.0f} (만원)'
    
    #concat the two dataframes
    df = pd.concat([actual_df, plan_df])

    fig = px.line(df, x="created_at", y="repayment_ratio", title="대출상환 진도율", markers=True, color='type', labels={'created_at': '월', 'repayment_ratio': '상환비율'}, range_x=[df['created_at'].min(), df['created_at'].max()])
    fig.add_annotation(x=ref_date, y=actual_repayment_ratio, text=annontated_text, showarrow=True, arrowhead=1, font=dict(size=16))

    # Create a JSON representation of the graph
    graphJSON = fig.to_json()
    return graphJSON