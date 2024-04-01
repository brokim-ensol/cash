from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Optional


class RepaymentFoam(FlaskForm):
    category = StringField(
        "카테고리", validators=[DataRequired("카테고리를 입력하세요.")]
    )
    amount = IntegerField(
        "상환금액(만원)", validators=[DataRequired("상환금액을 숫자(단위 :만원)로 입력하세요.")]
    )
    created_at = DateField("상환일", validators=[Optional()])
    remark = TextAreaField("비고", validators=[Optional()])
