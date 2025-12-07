from extensions import db
from models.category import UserCategory, SystemCategory

class CategoryController():

    @staticmethod
    def create_category(name, user_id, is_system= False):
        pass

    @staticmethod
    def get_category_by_name(name):
        category =  SystemCategory.query.filter_by(name= name).first()

        if category:
            return category
        
        category = UserCategory.query.filter_by(name= name).first()

        if category:
            return category
        
        return None



