from openapi_server import config
from datetime import datetime

db = config.db
ma = config.ma


#Status Class/Model
# noinspection PyUnresolvedReferences
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(10))
    pet_status = db.relationship('Pet', backref='status', lazy=True)
    order_status = db.relationship('Order', backref='status', lazy=True)

    def __init__(self, value):
        self.dis = dis
        self.value = value


class StatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'value')


status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)


#Category Class/Model
# noinspection PyUnresolvedReferences
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    cat_name = db.Column(db.String(100), unique=True)
    pet_category = db.relationship('Pet', backref='category', lazy=True)

    def __init__(self, id, cat_name):
        self.id = id
        self.cat_name = cat_name


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'cat_name')


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


#Order Class/Model
# noinspection PyUnresolvedReferences
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    pet_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    shipdate = db.Column(db.DateTime, default=datetime.utcnow)
    complete = db.Column(db.Boolean, default=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

    def __init__(self, id, pet_id, quantity, shipdate, complete, status_id):
        self.id =id
        self.pet_id = pet_id
        self.quantity = quantity
        self.shipdate = shipdate
        self.complete = complete
        self.status_id = status_id


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pet_id', 'quantity', 'shipdate', 'complete', 'status_id')


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# noinspection PyUnresolvedReferences
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('pet_id', db.Integer, db.ForeignKey('pet.id'), primary_key=True)
)


# noinspection PyUnresolvedReferences
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    pet_name = db.Column(db.String(20), unique=True)
    photoURLs = db.relationship('PhotoURL', backref='pet', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('tags', lazy=True))

    def __init__(self, id, pet_name, category_id, status_id):
        self.id = id
        self.pet_name = pet_name
        self.category_id = category_id
        self.status_id = status_id


class PetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'pet_name', 'category_id', 'status_id')


pet_schema = PetSchema()
pets_schema = PetSchema(many=True)


#Tag Class/Model
# noinspection PyUnresolvedReferences
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    tag_name = db.Column(db.String(100))

    def __init__(self, id, tag_name):
        self.id = id
        self.tag_name = tag_name


class TagSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tag_name')


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


#PhotoURLs Class/Model
# noinspection PyUnresolvedReferences
class PhotoURL(db.Model):
    url = db.Column(db.String(255), primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __init__(self, url, pet_id):
        self.url = url
        self.pet_id = pet_id


class PhotoURLsSchema(ma.Schema):
    class Meta:
        fields = ('url', 'pet_id')


photourl_schema = PhotoURLsSchema()
photourls_schema = PhotoURLsSchema(many=True)


#User Class/Model
# noinspection PyUnresolvedReferences
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(15), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    userstatus = db.Column(db.Integer)

    def __init__(self, id, username, firstname, lastname, email, password, phone, userstatus):
        self.id = id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone
        self.userstatus = userstatus


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'firstname', 'lastname', 'email', 'password', 'phone', 'userstatus')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
