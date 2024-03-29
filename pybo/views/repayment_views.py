from flask import Blueprint, render_template, request, url_for
from datetime import datetime
from pybo.models import Repayment, Balance
from pybo import db
from werkzeug.utils import redirect

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
    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        if request.form["remark"]:
            remark = request.form["remark"]
        else:
            remark = None
        now = datetime.now()
        repayment = Repayment(
            category=category, amount=amount, created_at=now, remark=remark
        )
        db.session.add(repayment)
        # query latest Balance
        latest_balance = Balance.query.order_by(Balance.created_at.desc()).first()
        if latest_balance is None:
            new_balance = int(amount)
        else:
            new_balance = latest_balance.balance - int(amount)
        balance = Balance(
            repayment_id=repayment.id,
            balance=new_balance,
            created_at=now,
            remark=remark,
        )
        repayment.balance_set.append(balance)
        db.session.commit()
        return redirect(url_for("repayment.detail", repayment_id=repayment.id))
    elif request.method == "GET":
        return render_template("repayment/repayment_create.html")
