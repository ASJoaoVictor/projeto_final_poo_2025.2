from extensions import db
from models.goal import Goal
from datetime import datetime, timedelta
from utils.exceptions import ValorInvalidoError, MetaJaExisteError, MetaInexistenteError

class GoalController():
    """Controlador responsável pelo gerenciamento de metas financeiras (Goals)."""
    
    @staticmethod
    def create_goal(goal_name, target_amount, user_id, duration, unit, category_id=None):
        """Cria uma nova meta financeira ou reativa uma meta antiga arquivada.

        Calcula o prazo final (deadline) com base na duração e unidade fornecidas.
        Se uma meta com o mesmo nome já existir e estiver inativa, ela será reativada
        e atualizada.

        Args:
            goal_name (str): O nome descritivo da meta (ex: 'Viagem', 'Carro Novo').
            target_amount (float|str): O valor monetário que se deseja alcançar.
            user_id (int): O ID do usuário dono da meta.
            duration (int|str): O tempo de duração da meta.
            unit (str): A unidade de tempo ('monthly' para meses, 'yearly' para anos).
            category_id (int, optional): ID da categoria associada (se houver).

        Returns:
            Goal: O objeto da meta criada ou atualizada.

        Raises:
            ValorInvalidoError: Se o valor alvo ou a duração não forem números válidos.
            MetaJaExisteError: Se já existir uma meta ativa com o mesmo nome.
        """
        try:
            target_amount = float(target_amount)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Valor alvo inválido.")

        try:
            duration = int(duration)
        except (ValueError, TypeError):
            raise ValorInvalidoError("Duração inválida.")
        
        real_unit = 1 if unit == "monthly" else 12
        duration_in_month = duration * real_unit
        deadline = datetime.now() + timedelta(days=30 * duration_in_month)
        
        existing_goal = Goal.query.filter_by(
            user_id= user_id, 
            goal_name= goal_name
        ).first()


        if existing_goal and existing_goal.is_active:
            raise MetaJaExisteError("Já existe uma meta ativa com esse nome.") 
        
        if existing_goal:
            goal = existing_goal
            goal.is_active = True
            goal.target_amount = target_amount
            goal.created_at = datetime.now().date()
        else:
            goal = Goal(
                goal_name= goal_name,
                target_amount= target_amount,
                deadline= deadline,
                category_id= category_id,
                created_at= datetime.now().date(),
                user_id= user_id
            )

            db.session.add(goal)
            
        db.session.commit()

        return goal
    
    @staticmethod
    def get_goals_by_user(user_id):
        """Recupera todas as metas ativas de um usuário.

        Args:
            user_id (int): O ID do usuário.

        Returns:
            list[Goal]: Lista de objetos Goal que estão com is_active=True.
        """
        goals = Goal.query.filter_by(user_id= user_id, is_active= True).all()
        return goals

    @staticmethod
    def check_expired_goals(user_id):
        """Verifica e desativa metas cujo prazo final já expirou.

        Percorre todas as metas ativas do usuário e compara a data limite (deadline)
        com a data atual. Se o prazo venceu, define is_active como False.

        Args:
            user_id (int): O ID do usuário cujas metas serão verificadas.
        """
        goals = GoalController.get_goals_by_user(user_id)
        today = datetime.today().date()

        for goal in goals:
            if goal.deadline <= today and goal.is_active:
                goal.is_active = False
        db.session.commit()

    @staticmethod
    def delete_goal(goal_id, user_id):
        """Remove permanentemente uma meta do banco de dados.

        Verifica se a meta existe e pertence ao usuário antes de deletar.

        Args:
            goal_id (int): O ID da meta a ser removida.
            user_id (int): O ID do usuário solicitante.

        Returns:
            bool: True se a exclusão for bem-sucedida.

        Raises:
            MetaInexistenteError: Se a meta não for encontrada ou não estiver ativa.
        """
        goal = Goal.query.filter_by(
            id= goal_id,
            user_id= user_id,
            is_active= True
        ).first()

        if not goal:
            raise MetaInexistenteError("Meta inexistente.")
        
        db.session.delete(goal)
        #goal.is_active = False
        db.session.commit()

        return True
    
    @staticmethod
    def edit_goal(goal_id, user_id, new_name, new_target_amount):
        """Edita o nome e o valor alvo de uma meta existente.

        Realiza validações para garantir que o novo nome não conflite com
        outra meta ativa do mesmo usuário.

        Args:
            goal_id (int): O ID da meta a ser editada.
            user_id (int): O ID do usuário dono da meta.
            new_name (str): O novo nome desejado para a meta.
            new_target_amount (float|str): O novo valor alvo.

        Returns:
            Goal: O objeto da meta atualizado.

        Raises:
            MetaInexistenteError: Se a meta original não for encontrada.
            MetaJaExisteError: Se o novo nome já estiver em uso por outra meta.
            ValorInvalidoError: Se o novo valor alvo não for numérico.
        """
        goal = Goal.query.filter_by(
            id= goal_id,
            user_id= user_id,
            is_active= True
        ).first()

        if not goal:
            raise MetaInexistenteError("Meta inexistente.")

        goal_existing = Goal.query.filter_by(
            user_id= user_id,
            goal_name= new_name
        ).first()

        if goal_existing and goal_existing.id != goal.id:
            raise MetaJaExisteError("Já existe uma meta ativa com esse nome.")
        
        try:
            new_target_amount = float(new_target_amount)
        except:
            raise ValorInvalidoError("Valor alvo inválido.")

        goal.goal_name = new_name
        goal.target_amount = new_target_amount
        db.session.commit()

        return goal