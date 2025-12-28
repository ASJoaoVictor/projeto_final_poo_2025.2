from flask import Flask, redirect, url_for
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.wallet_routes import wallet_bp
from routes.transaction_routes import transaction_bp
from routes.category_routes import category_bp
from routes.goal_routes import goal_bp
from extensions import db, login_manager
from models.user import User
from utils import seeder

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "chave-super-secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #inicializa o banco de controle de sessão
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "warning"

    with app.app_context():
        db.create_all()         # cria tabelas
        seeder.seed_system_categories()  # popula categorias do sistema

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(goal_bp)

    @app.route("/")
    def default():
        return redirect("/auth/login")

    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)