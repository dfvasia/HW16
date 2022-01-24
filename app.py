from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import data
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(60))
    role = db.Column(db.String(60))
    phone = db.Column(db.String(60))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(60))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


db.create_all()

for data_user in data.users:
    new_user = User(
        id=data_user["id"],
        first_name=data_user["first_name"],
        last_name=data_user["last_name"],
        age=data_user["age"],
        email=data_user["email"],
        role=data_user["role"],
        phone=data_user["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

for data_order in data.orders:
    new_order = Order(
        id=data_order["id"],
        name=data_order["name"],
        description=data_order["description"],
        start_date=data_order["start_date"],
        end_date=data_order["end_date"],
        price=data_order["price"],
        customer_id=data_order["customer_id"],
        executor_id=data_order["executor_id"],
    )
    db.session.add(new_order)
    db.session.commit()


for data_offer in data.offers:
    new_offer = Offer(
        id=data_offer["id"],
        order_id=data_offer["order_id"],
        executor_id=data_offer["executor_id"],
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/")
def start_page():
    list_user = [User.query.get(random.randint(0, User.query.count())) for _ in range(10)]
    list_order = [Order.query.get(random.randint(0, Order.query.count())) for _ in range(10)]
    list_offer = [Offer.query.get(random.randint(0, Offer.query.count())) for _ in range(10)]
    return render_template("main.html", s=list_user, s_1=list_order, s_2=list_offer)


@app.route("/users/")
def users_page():
    list_users = User.query.all()
    return render_template("users.html", s=list_users)


@app.route("/user/<int:id_user>")
def user_page(id_user: int):
    list_user = User.query.get(id_user)
    return render_template("user.html", s=list_user)


@app.route("/orders/")
def orders_page():
    list_orders = Order.query.all()
    return render_template("orders.html", s=list_orders)


@app.route("/order/<int:id_order>")
def order_page(id_order: int):
    list_order = Order.query.get(id_order)
    return render_template("order.html", s=list_order)


@app.route("/offers/")
def offers_page():
    list_offers = Offer.query.all()
    return render_template("offers.html", s=list_offers)


@app.route("/offer/<int:id_offers>")
def offer_page(id_offers: int):
    list_offer = Offer.query.get(id_offers)
    return render_template("offer.html", s=list_offer)


if __name__ == '__main__':
    app.run(debug=True)
