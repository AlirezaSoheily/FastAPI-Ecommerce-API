from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.models import Category, User


def initialize_app_data(db: Session) -> None:
    """Run required idempotent initialization tasks at startup."""
    _create_super_admin(db)
    _seed_default_categories(db)


def _create_super_admin(db: Session) -> None:
    username = settings.init_superadmin_username
    email = settings.init_superadmin_email
    password = settings.init_superadmin_password

    if not username or not email or not password:
        return

    admin_exists = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if admin_exists:
        return

    db_user = User(
        id=None,
        full_name=settings.init_superadmin_full_name,
        username=username,
        email=email,
        password=get_password_hash(password),
        role="admin",
        is_active=True,
    )

    db.add(db_user)
    db.commit()


def _seed_default_categories(db: Session) -> None:
    configured_categories = [
        name.strip()
        for name in settings.init_default_categories.split(",")
        if name.strip()
    ]

    if not configured_categories:
        return

    existing_categories = {
        category.name
        for category in db.query(Category).filter(Category.name.in_(configured_categories)).all()
    }

    categories_to_add = [
        Category(name=name)
        for name in configured_categories
        if name not in existing_categories
    ]

    if not categories_to_add:
        return

    db.add_all(categories_to_add)
    db.commit()
