from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from pybo.models import Repayment, Balance
from pybo import db
from pybo.forms import RepaymentFoam
import pandas as pd
from sqlalchemy import update

bp = Blueprint("repayment", __name__, url_prefix="/repayment")


@bp.route("/list/")
def _list():
    page = request.args.get("page", type=int, default=1)  # 페이지
    repayment_list = Repayment.query.order_by(Repayment.created_at.desc())
    repayment_list = repayment_list.paginate(page=page, per_page=10)
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
        created_at = form.created_at.data
        remark = form.remark.data if form.remark.data else ""
        repayment = Repayment(
            category=form.category.data,
            amount=form.amount.data,
            created_at=created_at,
            remark=remark,
        )
        db.session.add(repayment)
        balance = Balance(
            repayment_id=repayment.id,
            repaid_dt=created_at,
            category=form.category.data,
        )
        repayment.balance = balance
        update_balance()
        return render_template("repayment/repayment_detail.html", repayment=repayment)
    return render_template("repayment/repayment_create.html", form=form)


@bp.route("/modify/<int:repayment_id>", methods=("GET", "POST"))
def modify(repayment_id):
    repayment = Repayment.query.get_or_404(repayment_id)
    if request.method == "POST":  # POST 요청
        form = RepaymentFoam()
        if form.validate_on_submit():
            form.populate_obj(repayment)
            repayment.modified_at = datetime.now().date()
            update_balance()
            db.session.commit()
            return redirect(url_for("repayment.detail", repayment_id=repayment_id))
    else:  # GET 요청
        form = RepaymentFoam(obj=repayment)
    return render_template("repayment/repayment_create.html", form=form)


@bp.route("/delete/<int:repayment_id>")
def delete(repayment_id):
    repayment = Repayment.query.get_or_404(repayment_id)
    db.session.delete(repayment)
    db.session.commit()
    return redirect(url_for("repayment._list"))


def update_balance():
    balance_list = Balance.query.all()
    # unpacking balance_list which is a list of Balance objects
    balance_data = [
        (
            balance.id,
            balance.repayment_id,
            balance.repayment.amount,
            balance.repaid_dt,
            balance.category,
        )
        for balance in balance_list
    ]
    balance_df = pd.DataFrame.from_records(
        balance_data,
        columns=["id", "repayment_id", "amount", "repaid_dt", "category"],
    )
    balance_df = balance_df.sort_values(by=["repaid_dt", "id"], ascending=[True, True])
    balance_df["balance"] = 32000 - balance_df["amount"].cumsum()
    balance_df["ratio"] = 1 - (balance_df["amount"].cumsum() / 32000)
    balance_df.drop(columns="amount", inplace=True)
    balance_list = balance_df.to_dict(orient="records")
    db.session.bulk_update_mappings(Balance, balance_list)
    db.session.commit()
