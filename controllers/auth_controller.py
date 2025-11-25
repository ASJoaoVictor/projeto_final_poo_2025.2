from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from extensions import db
from models.user import User

class AuthController():
    def login(username, password):
        if(username=="teste@gmail.com" and password == "123"):
            return True
        return False

    def register(email, password):
        #Verificar se user existe
        existing_user = User.query.filter_by(email= email).first()

        if existing_user:
            return None
        
        #Crifrar senha
        password_hash = generate_password_hash(password)

        #criar novo usuário
        new_user = User(email= email, password= password_hash)

        #salva no db
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def logoff():
        pass