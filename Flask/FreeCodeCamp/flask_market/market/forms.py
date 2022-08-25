from flask_wtf import FlaskForm
# str, password : 비밀번호 암호화, submit: 회원가입 목록 작성 후 submit
from wtforms import StringField, PasswordField, SubmitField
# 사용자가 제출한 양삭 유효성 검사
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import Member


# 회원가입 form
class RegisterForm(FlaskForm):

    # 회원가입시 id가 겹치면 생기는 IntegrityError 해결 -> id가 겹칠 시 처리방법
    # id를 입력하면, FlaskForm이 StringField 내의 id를 모두 검사 -> validation 조건을 확인 -> 중복 여부 판단
    def validate_id(self, id_to_check):
        # 같은 id가 이미 존재
        id = Member.query.filter_by(id=id_to_check.data).first()
        if id:
            raise ValidationError('ID already exists! Please try a different ID')

    def validate_rnum(self, rnum_to_check):
        # 같은 주민번호가 이미 존재
        rnum = Member.query.filter_by(rnum=rnum_to_check.data).first()
        if rnum:
            raise ValidationError('Register Number already exists! Please try a different register number')

    def validtae_phnum(self, phnum_to_check):
        phnum = Member.query.filter_by(phnum=phnum_to_check.data).first()
        if phnum:
            raise ValidationError('Phone Number already exists! Please try a different phone number')

    def validate_email(self, email_to_check):
        email = Member.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email')


    id      = StringField(label='User ID : ', validators=[Length(min=2, max=20), DataRequired()])
    pwd1    = PasswordField(label='Password : ', validators=[Length(min=5), DataRequired()])   # 만들 패스워드
    # 올바르게 입력했는지 확인용, pwd1과 일치하는지 확인
    pwd2    = PasswordField(label='Confirm Password : ',validators=[EqualTo('pwd1'), DataRequired()])
    name    = StringField(label='User Name : ')
    gender  = StringField(label='Gender : ')
    rnum    = StringField(label='Register Number : ')
    phnum   = StringField(label='Phone Number : ')
    address = StringField(label='Address : ')
    email   = StringField(label='Email Address : ', validators=[Email(), DataRequired()])
    submit  = SubmitField(label='Create Account')   # 작성한 개인정보 제출


class LoginForm(FlaskForm):
    id = StringField(label='ID : ', validators=[DataRequired()])
    password = StringField(label='Password : ', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseProductForm(FlaskForm):
    submit = SubmitField(label='Purchase Product!')

class SellProductForm(FlaskForm):
    submit = SubmitField(label='Sell Product!')