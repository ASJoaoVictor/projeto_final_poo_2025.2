from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from extensions import db
from models.user import User
from utils.exceptions import UsuarioJaExisteError, UsuarioInexistenteError, SenhasDiferentes

class AuthController():
    """Controlador responsável pelas operações de autenticação de usuários."""

    @staticmethod
    def login(email, password):
        """Autentica um usuário e inicia a sessão.

        Verifica se o usuário existe e se a senha corresponde ao hash salvo.
        Se as credenciais forem válidas, realiza o login via Flask-Login.

        Args:
            email (str): O endereço de email do usuário.
            password (str): A senha em texto plano.

        Returns:
            User: O objeto do usuário autenticado.

        Raises:
            UsuarioInexistenteError: Se o usuário não for encontrado ou a senha estiver incorreta.
        """
        existing_user = User.query.filter_by(email= email).first()

        if not existing_user:
            raise UsuarioInexistenteError("Usuário não encontrado.")
        
        if(existing_user.check_password(password)):
            login_user(existing_user)
            return existing_user
        
        raise UsuarioInexistenteError("Usuário ou senha inválidos.")

    @staticmethod
    def register(username, email, password, confirm_password):
        """Registra um novo usuário no sistema.

        Verifica duplicidade de email, cria o hash da senha e persiste
        o novo usuário no banco de dados.

        Args:
            username (str): O nome de usuário desejado.
            email (str): O endereço de email do usuário.
            password (str): A senha em texto plano para ser criptografada.
            confirm_password (str): A senha em texto para confirmar a senha.

        Returns:
            User: O objeto do novo usuário criado.

        Raises:
            UsuarioJaExisteError: Se já existir um usuário com o email fornecido.
            SenhasDiferentes: Se as senhas enviadas não forem iguais.
        """
        #Verificar se user existe
        existing_user = User.query.filter_by(email= email).first()

        if existing_user:
            raise UsuarioJaExisteError("Usuário com esse email já existe.")

        #verificar senha
        if not password == confirm_password:
            raise SenhasDiferentes("As senhas precisam serem iguais.")

        password_hash = generate_password_hash(password)

        #criar novo usuário
        new_user = User(username= username, email= email, _password= password_hash)

        #salva no db
        db.session.add(new_user)
        db.session.commit()

        return new_user

    def logout():
        """Encerra a sessão do usuário atual.

        Desloga o usuário utilizando o Flask-Login.

        Returns:
            bool: Retorna True após a execução do logout.
        """
        logout_user()
        return True