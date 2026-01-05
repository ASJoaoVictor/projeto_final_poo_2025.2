from extensions import db
from models.objective import Objective
from utils.exceptions import ValorInvalidoError, ObjetivoInexistenteError

class ObjectiveController():
    """Controlador responsável pelo gerenciamento de objetivos financeiros de curto e longo prazo."""
    
    @staticmethod
    def create_objective(objective_name, target_amount, user_id, icon, wallet_id, due_date=None):
        """Cria um novo objetivo financeiro e o associa a uma carteira.

        Valida se o valor alvo é numérico e positivo antes de persistir o
        novo objetivo no banco de dados.

        Args:
            objective_name (str): O nome descritivo do objetivo.
            target_amount (float|str): O valor que se deseja alcançar.
            user_id (int): O ID do usuário dono do objetivo.
            icon (str): Identificador do ícone (ex: um emoji '💰').
            wallet_id (int): O ID da carteira vinculada a este objetivo.
            due_date (datetime, optional): A data limite para alcançar o objetivo.

        Returns:
            Objective: A instância do objetivo recém-criado.

        Raises:
            ValorInvalidoError: Se o valor não for um número ou for menor/igual a zero.
        """
        try:
            target_amount = float(target_amount)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Valor inválido para o objetivo.")
        
        if target_amount <= 0:
            raise ValorInvalidoError("O valor do objetivo deve ser positivo.")

        objective = Objective(
            objective_name= objective_name,
            target_amount= target_amount,
            due_date= due_date,
            user_id= user_id,
            wallet_id= wallet_id,
            icon = icon
        )

        db.session.add(objective)
        db.session.commit()

        return objective

    @staticmethod
    def get_objectives_user(user_id):
        """Recupera todos os objetivos ativos de um usuário.

        Args:
            user_id (int): O ID do usuário.

        Returns:
            list[Objective]: Uma lista contendo os objetivos ativos encontrados.
        """
        return Objective.query.filter_by(user_id=user_id, is_active=True).all()

    @staticmethod
    def delete_objective(objective_id, user_id):
        """Remove permanentemente um objetivo do sistema.

        Verifica se o objetivo existe e pertence ao usuário especificado
        antes de removê-lo do banco de dados.

        Args:
            objective_id (int): O ID do objetivo a ser excluído.
            user_id (int): O ID do usuário solicitante (para validação de segurança).

        Returns:
            bool: Retorna True se a exclusão for bem-sucedida.

        Raises:
            ObjetivoInexistenteError: Se o objetivo não for encontrado ou não pertencer ao usuário.
        """
        objective = Objective.query.filter_by(id=objective_id, user_id=user_id).first()

        if not objective:
            raise ObjetivoInexistenteError("Objetivo não encontrado.")

        db.session.delete(objective)
        db.session.commit()
        return True

    @staticmethod
    def edit_objective(id, new_name, new_target_amount, new_due_date, new_icon, new_wallet_id, user_id):
        """Atualiza os dados de um objetivo existente.

        Busca o objetivo pelo ID e verifica se pertence ao usuário antes de aplicar as
        alterações. Permite editar nome, valor, data, ícone e carteira.

        Args:
            id (int): O ID do objetivo a ser editado.
            new_name (str): O novo nome do objetivo.
            new_target_amount (float|str): O novo valor alvo.
            new_due_date (datetime): A nova data limite.
            new_icon (str): O novo ícone visual (ex: emoji ou caractere).
            new_wallet_id (int): O ID da nova carteira vinculada.
            user_id (int): O ID do usuário dono do objetivo.

        Returns:
            Objective: O objeto do objetivo com os dados atualizados.

        Raises:
            ObjetivoInexistenteError: Se o objetivo não for encontrado ou não pertencer ao usuário.
            ValorInvalidoError: Se o novo valor alvo for inválido ou negativo.
        """
        objective = Objective.query.filter_by(id=id, user_id=user_id).first()
        if not objective:
            raise ObjetivoInexistenteError("Objetivo não encontrado.")
        
        try:
            new_target_amount = float(new_target_amount)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Valor inválido para o objetivo.")
        
        if new_target_amount <= 0:
            raise ValorInvalidoError("O valor do objetivo deve ser positivo.")

        objective.objective_name = new_name
        objective.target_amount = new_target_amount
        objective.due_date = new_due_date
        objective.icon = new_icon
        objective.wallet_id = new_wallet_id

        db.session.commit()
        return objective