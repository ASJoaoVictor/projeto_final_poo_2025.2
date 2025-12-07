from extensions import db

class Category(db.Model):
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
    __mapper_args__ = {
        "polymorphic_identity": "user"
    }

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable= True)

    def __repr__(self):
        return f"<UserCategory {self.name}>"

class SystemCategory(Category):
    __mapper_args__ = {
        "polymorphic_identity": "system"
    }

    is_default = db.Column(db.Boolean, default= True)

    def __repr__(self):
        return f"<SystemCategory {self.name}>"