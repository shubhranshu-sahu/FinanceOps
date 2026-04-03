from app.models.category import Category
from app.models import db

def create_category(data, user_id):
    existing = Category.query.filter_by(name=data["name"].strip().lower()).first()

    if existing:
        raise ValueError("Category already exists")

    category = Category(
        name=data["name"].strip().lower(),
        created_by=user_id
    )

    db.session.add(category)
    db.session.commit()

    return category

def get_categories(include_disabled=False):
    if include_disabled:
        return Category.query.all()
    return Category.query.filter_by(is_active=True).all()

def update_category_status(category_id, is_active):
    category = Category.query.get(category_id)

    if not category:
        raise ValueError("Category not found")

    category.is_active = is_active
    db.session.commit()

    return category

def update_category_name(category_id, new_name):
    clean_name = new_name.strip().lower()

    if not clean_name:
        raise ValueError("Category name cannot be empty")

    category = Category.query.get(category_id)
    if not category:
        raise ValueError("Category not found")
        
    existing = Category.query.filter_by(name=clean_name).first()
    if existing and existing.id != category_id:
        raise ValueError("Another category with this name already exists")

    category.name = clean_name
    db.session.commit()
    return category