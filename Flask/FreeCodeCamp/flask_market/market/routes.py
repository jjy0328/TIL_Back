# flash : built-in function that is going to help us to provide extra messages to our users
# request : Flask는 요청 데이터를 파싱해서 request 전역 객체에 저장. 이를 통해 데이터에 접근 가능
from flask import render_template, redirect, url_for, flash, request
from market import app
from market.models import Product, Member
from market.forms import RegisterForm, LoginForm, PurchaseProductForm, SellProductForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

# 임의의 데이터 보내는 decorator
################## Owner - products 연결
@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseProductForm()
    selling_form = SellProductForm()
    if request.method == "POST":
        # 구매 기능
        # product_modals의 input태그의 id, name과 같아야 함
        purchased_product = request.form.get('purchased_product')
        p_product_object = Product.query.filter_by(pname=purchased_product).first()
        if p_product_object:
            p_product_object.buy(current_user)
            flash(f"Congratulations! "
                  f"You purchased {p_product_object.pname} for {p_product_object.price}$", category='success')
        else:
            flash(f"Something went wrong with purchased {p_product_object.pname}", category="danger")

    # 상품 파는 기능
    sold_product = request.form.get('sold_product')
    s_product_object = Product.query.filter_by(pname=sold_product).first()
    if s_product_object:
        if current_user.can_sell(s_product_object):
            s_product_object.sell(current_user)
            flash(f"Congratulations! "
                  f"You sold {s_product_object.pname} back to market!", category='success')
        else:
            flash(f"Something went wrong with selling {s_product_object.pname}", category="danger")

        return redirect(url_for('market_page'))

    if request.method == "GET":
        products = Product.query.filter_by(owner=None)
        # 어떤 사용자가 어떤 품목을 샀는지 알 수 있는 query문
        owned_products = Product.query.filter_by(owner=current_user.id)
        return render_template('market.html', products=products,
                               purchase_form=purchase_form, owned_product=owned_products,
                               selling_form=selling_form)


@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    # 사용자가 submit 버튼을 눌렀는지 확인용
    # 유효성 검사 : 회원가입 조건을 충족하는지
    if form.validate_on_submit():
        # 회원가입에 필요한 인수
        member_to_create = Member(name     = form.name.data,
                                  id       = form.id.data,
                                  password = form.pwd1.data,   # password.setter로 넘어가 비밀번호를 암호로 decode한 후 저장
                                  gender   = form.gender.data,
                                  rnum     = form.rnum.data,
                                  phnum    = form.phnum.data,
                                  address  = form.address.data,
                                  email    = form.email.data)
        db.session.add(member_to_create)
        db.session.commit()
        # 다른 페이지로 넘어감
        # 연결되는 url을 하드코딩하는 것은 좋지 않기 때문에 route 자체를 url 자리에 넣어줌
        return redirect(url_for('market_page'))
    # 조건에 충족하지 않은 것들 잡아내기
    if form.errors != {} : # 유효성 검사에 에러가 없으면
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category="danger")

    return render_template('register.html', form=form)


# 로그인 기능
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    # 간편 로그인 관련 유효성 검사
    # 조건 1) 유저 아이디가 존재하는지    2) 존재하는 아이디의 패스워드가 일치하는지
    # .first() : grab the object of the member
    if form.validate_on_submit():
        # going to filter out member by the provided id
        attempted_member  = Member.query.filter_by(id=form.id.data).first()
        if attempted_member and attempted_member.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_member)
            flash(f"Success! You are logged in as: {attempted_member.id}", category='success')
            return redirect(url_for('market_page'))
        else:
            flash('ID and password are not match! Please try again', category='danger')

    # html 파일을 렌더링
    return render_template('login.html', form=form)


#로그아웃 기능
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    # 특정 주소로 접속. 주소에서 데이터를 처리하는 과정만 거치고 결과를 보여주거나 응용할 때 사용
    return redirect(url_for("home_page"))