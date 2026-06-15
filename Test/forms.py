from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, TextAreaField, SelectField,
    SubmitField, FloatField, BooleanField
)
from wtforms.validators import DataRequired, equal_to, length, Optional, NumberRange
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()
    ])
    password = PasswordField("Enter Password", validators=[
        DataRequired(),
        length(min=6, max=24)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        equal_to("password", message="Passwords do not match")
    ])
    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    login = SubmitField("Log In")


class ArtworkForm(FlaskForm):
    image = FileField("Upload Artwork Image", validators=[
        FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Images only!")
    ])
    title = StringField("Enter Artwork Title", validators=[DataRequired()])
    artist = StringField("Enter Artist Name", validators=[DataRequired()])
    category = SelectField("Select Category", choices=[
        ("", "Select Category"),
        ("Painting", "Painting"),
        ("Sculpture", "Sculpture"),
        ("Photography", "Photography"),
        ("Digital Art", "Digital Art"),
        ("Drawing", "Drawing"),
        ("Printmaking", "Printmaking"),
        ("Mixed Media", "Mixed Media"),
        ("Installation", "Installation"),
        ("Textile", "Textile"),
        ("Other", "Other"),
    ], validators=[DataRequired()])
    description = TextAreaField("Enter Description", validators=[DataRequired()])
    for_sale = BooleanField("For Sale")
    price = FloatField("Price ($)", validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField("Save Artwork")


class CommentForm(FlaskForm):
    text = TextAreaField("Add a comment", validators=[DataRequired(), length(max=500)])
    submit = SubmitField("Post Comment")


class RatingForm(FlaskForm):
    value = SelectField("Your Rating", choices=[
        ("5", "5 - Excellent"),
        ("4", "4 - Great"),
        ("3", "3 - Good"),
        ("2", "2 - Fair"),
        ("1", "1 - Poor"),
    ], validators=[DataRequired()])
    submit = SubmitField("Rate")
