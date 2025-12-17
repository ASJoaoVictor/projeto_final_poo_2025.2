from extensions import db
from models.category import UserCategory, SystemCategory

class CategoryController():

    @staticmethod
    def create_category(name, user_id, is_system= False):
        exising_category = UserCategory.query.filter_by(
            name= name, 
            user_id= user_id
            ).first()
        print(name)
        if exising_category:
            return None

        new_category = UserCategory(
            name= name,
            user_id= user_id
        )

        db.session.add(new_category)
        db.session.commit()

        return new_category

    @staticmethod
    def get_user_categories(user_id):
        return UserCategory.query.filter_by(user_id= user_id).all()
    
    @staticmethod
    def edit_category(category_id, new_name, user_id):
        category = UserCategory.query.filter_by(
            id= category_id,
            user_id= user_id
        ).first()

        if not category:
            return None
        
        category.name = new_name
        db.session.commit()

        return category
    
    @staticmethod
    def delete_category(category_id, user_id):
        category = UserCategory.query.filter_by(
            id= category_id,
            user_id= user_id
        ).first()

        if not category:
            return False
        
        db.session.delete(category)
        db.session.commit()

        return True


