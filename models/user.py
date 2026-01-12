from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """Modelo de dados que representa um usuário registrado no sistema.

    Esta classe atua como a entidade proprietária dos dados. Carteiras, Transações, 
    Metas e Categorias Personalizadas são todas vinculadas a um `id` de usuário.

    A herança de `UserMixin` fornece implementações padrão para integração com 
    o Flask-Login (autenticação de sessão), incluindo propriedades como 
    `is_authenticated` e `is_active`.

    Attributes:
        id (int): Identificador único do usuário (Primary Key).
        username (str): Nome de exibição do usuário (usado em saudações no dashboard).
        email (str): Endereço de e-mail único usado como chave de login.
        password (str): Hash da senha criptografada.
                        ATENÇÃO: Este campo deve armazenar apenas o hash (ex: bcrypt),
                        nunca a senha em texto plano.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(120), unique= True, nullable= False)
    _password = db.Column(db.String(255), nullable= False)

    @property
    def password(self):
        raise AttributeError("A senha não é um atributo legível!")

    @password.setter
    def password(self, password_value):
        self._password = password_value

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f"<User {self.email}>"