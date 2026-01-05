from extensions import db
from models.category import UserCategory
from utils.exceptions import CategoriaJaExisteError, CarteiraInexistenteError

class CategoryController():
    """Controlador responsável pelo gerenciamento de categorias personalizadas do usuário."""

    @staticmethod
    def create_category(name, user_id, is_system= False):
        """Cria uma nova categoria para o usuário especificado.

        Verifica se já existe uma categoria com o mesmo nome para este usuário
        antes de criar.

        Args:
            name (str): O nome da nova categoria.
            user_id (int): O ID do usuário dono da categoria.
            is_system (bool, optional): Define se é uma categoria padrão do sistema. 
                Padrão é False.

        Returns:
            UserCategory: O objeto da categoria recém-criada.

        Raises:
            CategoriaJaExisteError: Se o usuário já possuir uma categoria com este nome.
        """

        exising_category = UserCategory.query.filter_by(
            name= name, 
            user_id= user_id
            ).first()

        if exising_category:
            raise CategoriaJaExisteError("Categoria com esse nome já existe.")

        new_category = UserCategory(
            name= name,
            user_id= user_id
        )

        db.session.add(new_category)
        db.session.commit()

        return new_category

    @staticmethod
    def get_user_categories(user_id):
        """Recupera todas as categorias pertencentes a um usuário.

        Args:
            user_id (int): O ID do usuário para filtrar as categorias.

        Returns:
            list[UserCategory]: Uma lista contendo os objetos das categorias encontradas.
        """
        return UserCategory.query.filter_by(user_id= user_id).all()
    
    @staticmethod
    def edit_category(category_id, new_name, user_id):
        """Atualiza o nome de uma categoria existente.

        Busca a categoria pelo ID e valida a propriedade. Também verifica se o 
        novo nome já está sendo usado por outra categoria do mesmo usuário
        para evitar duplicatas.

        Args:
            category_id (int): O ID da categoria a ser editada.
            new_name (str): O novo nome para a categoria.
            user_id (int): O ID do usuário solicitante.

        Returns:
            UserCategory: O objeto da categoria atualizado.

        Raises:
            CategoriaInexistenteError: Se a categoria não for encontrada ou não pertencer ao usuário.
            CategoriaJaExisteError: Se o usuário já possuir outra categoria com o novo nome.
        """
        category = UserCategory.query.filter_by(
            id= category_id,
            user_id= user_id
        ).first()

        if not category:
            raise CarteiraInexistenteError("Categoria não encontrada.")
        
        category_existing = UserCategory.query.filter_by(
            name= new_name,
            user_id= user_id
        ).first()     

        if category_existing and category_existing.id != category_id:
            raise CategoriaJaExisteError("Já existe uma categoria com esse nome.")
        
        category.name = new_name
        db.session.commit()

        return category
    
    @staticmethod
    def delete_category(category_id, user_id):
        """Remove uma categoria do sistema.

        Busca a categoria pelo ID e verifica a propriedade do usuário
        antes de excluí-la do banco de dados.

        Args:
            category_id (int): O ID da categoria a ser excluída.
            user_id (int): O ID do usuário solicitante.

        Returns:
            bool: Retorna True se a exclusão for bem-sucedida.

        Raises:
            CarteiraInexistenteError: Se a categoria não for encontrada ou não pertencer ao usuário.
        """
        category = UserCategory.query.filter_by(
            id= category_id,
            user_id= user_id
        ).first()

        if not category:
            raise CarteiraInexistenteError("Categoria não encontrada.")

        db.session.delete(category)
        db.session.commit()
        return True


