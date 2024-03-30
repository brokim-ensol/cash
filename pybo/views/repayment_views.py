from flask import Blueprint, render_template, request, url_for
from datetime import datetime
from pybo.models import Repayment, Balance
from pybo import db
from werkzeug.utils import redirect
from pybo.forms import RepaymentFoam
from pybo.models import Repayment

bp = Blueprint("repayment", __name__, url_prefix="/repayment")


@bp.route("/list/")
def _list():
    repayment_list = Repayment.query.order_by(Repayment.created_at.desc())
    return render_template(
        "repayment/repayment_list.html", repayment_list=repayment_list
    )


@bp.route("/detail/<int:repayment_id>/")
def detail(repayment_id):
    repayment = Repayment.query.get_or_404(repayment_id)
    return render_template("repayment/repayment_detail.html", repayment=repayment)


@bp.route("/create/", methods=("POST", "GET"))
def create():
    form = RepaymentFoam()
    if request.method == "POST" and form.validate_on_submit():
        created_at = form.created_at.data if form.created_at.data else datetime.now()
        remark = form.remark.data if form.remark.data else None
        repayment = Repayment(
            category=form.category.data,
            amount=form.amount.data,
            created_at=created_at,
            remark=remark,
        )
        db.session.add(repayment)
        latest_balance = Balance.query.order_by(Balance.created_at.desc()).first()
        if latest_balance is None:
            new_balance = int(form.amount.data)
        else:
            new_balance = latest_balance.balance - int(form.amount.data)
        balance = Balance(
            repayment_id=repayment.id,
            balance=new_balance,
            created_at=created_at,
            remark=remark,
        )
        repayment.balance_set.append(balance)
        db.session.commit()
        return render_template("repayment/repayment_detail.html", repayment=repayment)
    return render_template("repayment/repayment_create.html", form=form)
