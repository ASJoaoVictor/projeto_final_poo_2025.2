from models.category import SystemCategory
from extensions import db


def seed_system_categories():  
    default_categories = [
        "Depósito inicial",
        "Saque final",
    ]

    for cat_name in default_categories:
        existing = SystemCategory.query.filter_by(name= cat_name).first()

        if existing:
            print(f"[OK] Categoria '{cat_name}' já existe.")
            continue
        
        new_cat = SystemCategory(name= cat_name, is_default= True)
        db.session.add(new_cat)
        print(f"[OK] Categoria '{cat_name}' criada.")

    db.session.commit()