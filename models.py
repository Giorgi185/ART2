from ext import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("artwork_id", db.Integer, db.ForeignKey("artworks.id"), primary_key=True),
)


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String(), default="Guest")

    artworks = db.relationship("Artwork", backref="owner", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    ratings = db.relationship("Rating", backref="user", lazy=True)
    favorite_artworks = db.relationship(
        "Artwork",
        secondary=favorites,
        backref=db.backref("favorited_by", lazy="dynamic"),
        lazy="dynamic",
    )

    def is_admin(self):
        return self.role == "Admin"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Artwork(db.Model, BaseModel):
    __tablename__ = "artworks"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    artist = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String())

    price = db.Column(db.Float(), nullable=True)
    for_sale = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=True)

    comments = db.relationship("Comment", backref="artwork", lazy=True, cascade="all, delete-orphan")
    ratings = db.relationship("Rating", backref="artwork", lazy=True, cascade="all, delete-orphan")

    @property
    def average_rating(self):
        if not self.ratings:
            return None
        return round(sum(r.value for r in self.ratings) / len(self.ratings), 1)

    @property
    def rating_count(self):
        return len(self.ratings)


class Comment(db.Model, BaseModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    artwork_id = db.Column(db.Integer(), db.ForeignKey("artworks.id"), nullable=False)


class Rating(db.Model, BaseModel):
    __tablename__ = "ratings"

    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.Integer(), nullable=False)

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    artwork_id = db.Column(db.Integer(), db.ForeignKey("artworks.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "artwork_id", name="unique_user_artwork_rating"),)
