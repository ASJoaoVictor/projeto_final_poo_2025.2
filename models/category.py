from extensions import db

class Category(db.Model):
    """Classe base para categorias financeiras (Herança de Tabela Única).

    Esta classe define a estrutura comum para todas as categorias e utiliza o padrão
    'Polymorphic Identity' do SQLAlchemy. Todos os registros (sejam de sistema ou de usuário)
    são armazenados na tabela 'categories', diferenciados pela coluna 'type'.

    Attributes:
        id (int): Identificador único da categoria.
        name (str): O nome visível da categoria (ex: 'Alimentação', 'Salário').
        type (str): Coluna discriminadora usada pelo SQLAlchemy para identificar 
                    se a instância é uma 'SystemCategory' ou 'UserCategory'.
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable= False)

    type = db.Column(db.String(20), nullable= False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "category"
    }

    def __repr__(self):
        return f"<Category {self.name}>"
    
class UserCategory(Category):
    """Subclasse que representa categorias personalizadas criadas por usuários.

    Estas categorias são privadas e visíveis apenas para o usuário que as criou.
    Herda todos os atributos de `Category` e adiciona o vínculo com o `User`.

    Attributes:
        user_id (int): Chave estrangeira que vincula a categoria ao usuário proprietário.
                       Se for NULL, a categoria fica 'órfã' (o que deve ser evitado).
    """
    __mapper_args__ = {
        "polymorphic_identity": "user"
    }

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable= True)

    def __repr__(self):
        return f"<UserCategory {self.name}>"

class SystemCategory(Category):
    """Subclasse para categorias de uso exclusivo do sistema (Internal Use Only).

    Estas categorias são estritamente reservadas para operações automáticas do backend
    (ex: Depósito inicial).
    
    ATENÇÃO: Instâncias desta classe NÃO devem ser exibidas para seleção do usuário 
    final em interfaces de criação de transação ou metas.

    Attributes:
        is_default (bool): Flag para configurações internas (ex: categorias imutáveis).
    """
    __mapper_args__ = {
        "polymorphic_identity": "system"
    }

    is_default = db.Column(db.Boolean, default= True)

    def __repr__(self):
        return f"<SystemCategory {self.name}>"