from flask import Flask, render_template, request
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


@app.route("/users", methods=['GET', 'POST'])
def users_page():
    if request.method == "GET":
        list_users = User.query.all()
        return render_template("users.html", s=list_users)
    elif request.method == "POST":
        new_user = User(
            first_name=request.form.get("append_user_first_name"),
            last_name=request.form.get("append_user_last_name"),
            age=int(request.form.get("append_user_age")),
            email=request.form.get("append_user_email"),
            role=request.form.get("append_user_role"),
            phone=request.form.get("append_user_phone"),
        )
        db.session.add(new_user)
        db.session.commit()
        return f"готово", 204


@app.route("/user/<int:id_user>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def user_page(id_user: int):
    if request.method == "GET":
        list_user = User.query.get(id_user)
        return render_template("user.html", s=list_user)

    elif request.method == "POST":
        if request.form['btn_identifier'] == 'id_identifier':
            list_temp_1 = {
                1: str(request.form.get("append_user_first_name")),
                2: str(request.form.get("append_user_last_name")),
                3: int(request.form.get("append_user_age")),
                4: str(request.form.get("append_user_email")),
                5: str(request.form.get("append_user_role")),
                6: str(request.form.get("append_user_phone")),
            }
            u = User.query.get(id_user)
            u.first_name = list_temp_1[1],
            u.last_name = list_temp_1[2],
            u.age = list_temp_1[3],
            u.email = list_temp_1[4],
            u.role = list_temp_1[5],
            u.phone = list_temp_1[6],
            db.session.add(u)
            db.session.commit()

        elif request.form['btn_identifier'] == 'idx_identifier':
            del_user = User.query.get(id_user)
            db.session.delete(del_user)
            db.session.commit()
        return f"готово", 204


@app.route("/orders/", methods=['GET', 'POST', 'DELETE', 'PUT'])
def orders_page():
    if request.method == "GET":
        list_orders = Order.query.all()
        return render_template("orders.html", s=list_orders)

    elif request.method == "POST":
        new_order = Order(
            name=request.form.get("name"),
            description=request.form.get("description"),
            start_date=int(request.form.get("start_date")),
            end_date=request.form.get("end_date"),
            price=request.form.get("price"),
            customer_id=request.form.get("customer_id"),
            executor_id=request.form.get("executor_id"),
        )
        db.session.add(new_order)
        db.session.commit()
        return f"готово", 204


@app.route("/order/<int:id_order>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def order_page(id_order: int):
    if request.method == "GET":
        list_order = Order.query.get(id_order)
        return render_template("order.html", s=list_order)

    elif request.method == "POST":
        if request.form['btn_identifier'] == 'id_identifier':
            list_temp = {
                1: str(request.form.get("name")),
                2: str(request.form.get("description")),
                3: int(request.form.get("start_date")),
                4: str(request.form.get("end_date")),
                5: str(request.form.get("price")),
                6: str(request.form.get("customer_id")),
                7: str(request.form.get("executor_id")),
            }
            order = Order.query.get(id_order)
            order.name = list_temp[1],
            order.description = list_temp[2],
            order.start_date = list_temp[3],
            order.end_date = list_temp[4],
            order.price = list_temp[5],
            order.customer_id = list_temp[6],
            order.executor_id = list_temp[7],
            db.session.add(order)
            db.session.commit()

        elif request.form['btn_identifier'] == 'idx_identifier':
            del_user = Order.query.get(id_order)
            db.session.delete(del_user)
            db.session.commit()
        return f"готово", 204


@app.route("/offers/", methods=['GET', 'POST', 'DELETE', 'PUT'])
def offers_page():
    if request.method == "GET":
        list_offers = Offer.query.all()
        return render_template("offers.html", s=list_offers)

    elif request.method == "POST":
        new_offer = Offer(
            order_id=request.form.get("order_id"),
            executor_id=request.form.get("executor_id"),
        )
        db.session.add(new_offer)
        db.session.commit()
        return f"готово"


@app.route("/offer/<int:id_offers>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def offer_page(id_offers: int):
    if request.method == "GET":
        list_offer = Offer.query.get(id_offers)
        return render_template("offer.html", s=list_offer)

    elif request.method == "POST":
        if request.form['btn_identifier'] == 'id_identifier':
            list_temp = {
                1: int(request.form.get("order_id")),
                2: int(request.form.get("executor_id")),
            }
            of = Offer.query.get(id_offers)
            of.order_id = list_temp[1],
            of.executor_id = list_temp[2],
            db.session.add(of)
            db.session.commit()
        elif request.form['btn_identifier'] == 'idx_identifier':
            del_user = Offer.query.get(id_offers)
            db.session.delete(del_user)
            db.session.commit()
        return f"готово", 204


if __name__ == '__main__':
    app.run(debug=True)
