from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from extensions import db
from models.user import User

class AuthController():
    def login(email, password):
        existing_user = User.query.filter_by(email= email).first()

        if not existing_user:
            return None
        
        if(check_password_hash(existing_user.password, password)):
            login_user(existing_user)
            return existing_user
        
        return None

    def register(username, email, password):
        #Verificar se user existe
        existing_user = User.query.filter_by(email= email).first()

        if existing_user:
            return None
        
        #Crifrar senha
        password_hash = generate_password_hash(password)

        #criar novo usuário
        new_user = User(username= username, email= email, password= password_hash)

        #salva no db
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def logout():
        logout_user()
        return True