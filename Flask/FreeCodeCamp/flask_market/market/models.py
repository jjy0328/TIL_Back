from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

#  - is_authenticated
# 인증된 경우 True, 그렇지 않은 경우 False
#  - is_active
# 계정이 활성화된 경우 True, 그렇지 않은 경우 False
#  - is_anonymous
# 익명 사용자는 True, 그렇지 않은 경우 False
#  - get_id()
# 사용자의 고유 식별 문자를 보여주는 메소드
# => 이 4가지의 구현이 일반적이므로 Flask-Login은 이에 적합한 사용자 모델 클래스 구현을 지원하는 믹스 인 클래스를 제공


@login_manager.user_loader
def load_user(id):
    return Member.query.get(id)

# parameter로 UserMixin을 넣음으로써 flask_login이 지원하는 클래스 상속받음
class Member(db.Model, UserMixin):
    id       = db.Column(db.String(length=20),   nullable=False, primary_key=True)
    pwd_hash = db.Column(db.String(length=60),   nullable=False) # 암호화 필요
    name     = db.Column(db.String(length=20),   nullable=False)
    rnum     = db.Column(db.String(length=20),   nullable=False, unique=True)
    gender   = db.Column(db.Integer(),           nullable=False)
    phnum    = db.Column(db.String(length=20),   nullable=False, unique=True)
    address  = db.Column(db.String(length=1024), nullable=False)
    email    = db.Column(db.String(length=1024), nullable=False, unique=True)

    # relationship field : 두 테이블 간의 관계 정립
    # member가 product를 소유함을 보여줌
    # backref : member model 역 참조 (product의 소유자를 알 수 있음)
    # lazy = True : sqlalchmy가 하나 이상의 수정사항을 인식
    products = db.relationship('Product', backref='owned_member', lazy=True)


    # 예산 10,000형식으로 만들기
    # @property
    # def prettier_budget(self):
    #     if len(str(self.budget)) >= 4:
    #         return f'{str(self.budget)[:-3]}, {str(self.budget)[-3:]}$'
    #     else:
    #         return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    # 비밀번호 암호화하여 저장
    @password.setter
    def password(self, plain_text_password):
        self.pwd_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # 로그인시 암호화된 패스워드와의 일치성을 확인할 수 없어, 비밀번호가 일치한지 확인해주는 함수를 넣음
    # 비밀번호가 일치하면 true, 일치하지 않으면 false 반
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.pwd_hash, attempted_password)

    ###### 조건 생각해보기
    # def can_purchase(self):
    #     return

    # 품목 팔기
    # owner가 가지고 있는지만 확인하면 됨
    def can_sell(self, purchase_obj):
        return purchase_obj in self.products


# DB table로 변환
class Product(db.Model):
    pnum   = db.Column(db.Integer(), primary_key=True)
    pname  = db.Column(db.String(length=30), nullable=False, unique=True)
    detail = db.Column(db.String(length=1024), nullable=False, unique=True)
    price  = db.Column(db.Integer(), nullable=False)
    image  = db.Column(db.String(length=1024), nullable=False, unique=True)
    #fk 지정
    owner = db.Column(db.Integer(), db.ForeignKey('member.id'))
    def __rerp__(self):
        return f"Product {self.pname}"

    def buy(self, member):
        self.owner = member.id
        db.session.commit()

    def sell(self, member):
        # assign ownership to nobody
        self.owner = None
        db.session.commit()