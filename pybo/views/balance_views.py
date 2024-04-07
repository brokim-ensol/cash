from flask import Blueprint, render_template, request
from pybo.models import Balance

bp = Blueprint('balance', __name__, url_prefix='/balance')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    balance_list = Balance.query.order_by(Balance.repaid_dt.desc(), Balance.balance.asc())
    balance_list = balance_list.paginate(page=page, per_page=10)
    return render_template('balance/balance_list.html', balance_list=balance_list)


@bp.route('/detail/<int:balance_id>/')
def detail(balance_id):
    balance = Balance.query.get_or_404(balance_id)
    return render_template('balance/balance_detail.html', balance=balance)