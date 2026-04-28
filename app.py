from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
import bcrypt

# ROTAS DE REFEIÇÃO
from routes.meal_routes import meal_bp


def create_app():
    app = Flask(__name__)

    # ======================
    # CONFIGURAÇÕES
    # ======================
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/dietss_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # ======================
    # BANCO DE DADOS
    # ======================
    db.init_app(app)

    # ======================
    # LOGIN MANAGER
    # ======================
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ======================
    # ROTAS DE USUÁRIO
    # ======================

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if username and password:
            hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'Usuário criado com sucesso'}), 200

        return jsonify({'message': 'Dados inválidos'}), 400

    # ======================
    # LOGIN
    # ======================
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Credenciais inválidas'}), 400

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(
            password.encode(),
            user.password.encode()
        ):
            login_user(user)
            return jsonify({'message': 'Login realizado com sucesso'}), 200

        return jsonify({'message': 'Credenciais inválidas'}), 400

    # ======================
    # LOGOUT
    # ======================
    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logout realizado com sucesso'}), 200

    # ======================
    # REGISTRO DAS ROTAS DE REFEIÇÃO
    # ======================
    app.register_blueprint(meal_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)