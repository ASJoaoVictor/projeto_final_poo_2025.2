from flask import Flask, redirect
from routes.auth_routes import auth_bp
from extensions import db, login_manager
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "chave-super-secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #inicializa o banco de controle de sessão
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp)

    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)