from extensions import db
from models.category import UserCategory, SystemCategory

class CategoryController():

    @staticmethod
    def create_category(name, user_id, is_system= False):
        pass

    @staticmethod
    def get_user_categories(user_id):
        return UserCategory.query.filter_by(user_id= user_id).all()



