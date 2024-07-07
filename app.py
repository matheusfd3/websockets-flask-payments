from flask import Flask, jsonify, request
from repository.database import db
from db_models.payment import Payment
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

db.init_app(app)

@app.route('/payments/pix', methods=['POST'])
def create_pix_payment():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({'message': 'Value is required!'}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'], expiration_date=expiration_date)

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({'message': 'Pix payment created!',
                    'payment': new_payment.to_dict()}), 201

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirm_pix_payment():
    return jsonify({'message': 'Pix payment confirmed!'}), 201

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def page_pix_payment(payment_id):
    return f'Pix payment {payment_id} page!', 200

if __name__ == '__main__':
    app.run(debug=True)