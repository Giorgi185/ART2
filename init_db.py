from ext import app, db
from models import Artwork, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(
        username="admin",
        password=generate_password_hash("admin123"),
        role="Admin"
    )
    admin.create()


    print("Database initialized successfully!")
    print("Admin login -> username: admin  |  password: admin123")
