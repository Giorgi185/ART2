from ext import app, db
from flask import render_template, redirect, flash, request, url_for
from forms import RegisterForm, LoginForm, ArtworkForm, CommentForm, RatingForm
from models import Artwork, User, Comment, Rating
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


ARTISTS = [
    {"wiki": "https://en.wikipedia.org/wiki/Leonardo_da_Vinci", "name": "Leonardo da Vinci", "info": "Italian artist, High Renaissance style", "img": "art1.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Vincent_van_Gogh", "name": "Vincent van Gogh", "info": "Dutch painter, Post-Impressionism style", "img": "art2.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Pablo_Picasso", "name": "Pablo Picasso", "info": "Spanish artist, Cubism style", "img": "art3.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Michelangelo", "name": "Michelangelo", "info": "Italian artist, Renaissance style", "img": "art4.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Rembrandt", "name": "Rembrandt", "info": "Dutch painter, Baroque style", "img": "art5.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Claude_Monet", "name": "Claude Monet", "info": "French painter, Impressionism style", "img": "art6.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Salvador_Dal%C3%AD", "name": "Salvador Dalí", "info": "Spanish artist, Surrealism style", "img": "art7.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Edgar_Degas", "name": "Edgar Degas", "info": "French painter, Impressionism style", "img": "art8.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Raphael", "name": "Raphael", "info": "Italian painter, High Renaissance style", "img": "art9.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Caravaggio", "name": "Caravaggio", "info": "Italian painter, Baroque style", "img": "art10.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Frida_Kahlo", "name": "Frida Kahlo", "info": "Mexican artist, Surrealism and Realism", "img": "art11.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Andy_Warhol", "name": "Andy Warhol", "info": "American artist, Pop Art style", "img": "art12.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Jackson_Pollock", "name": "Jackson Pollock", "info": "American painter, Abstract Expressionism", "img": "art13.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Gustav_Klimt", "name": "Gustav Klimt", "info": "Austrian artist, Symbolism style", "img": "art14.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Johannes_Vermeer", "name": "Johannes Vermeer", "info": "Dutch painter, Baroque style", "img": "art15.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Paul_C%C3%A9zanne", "name": "Paul Cézanne","info": "French painter, Post-Impressionism", "img": "art16.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Henri_Matisse", "name": "Henri Matisse", "info": "French artist, Fauvism","img": "art17.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Edvard_Munch", "name": "Edvard Munch","info": "Norwegian painter, Expressionism", "img": "art18.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Georgia_O%27Keeffe", "name": "Georgia O'Keeffe","info": "American artist, Modernism", "img": "art19.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Wassily_Kandinsky", "name": "Wassily Kandinsky","info": "Abstract art pioneer", "img": "art20.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Sandro_Botticelli", "name": "Sandro Botticelli","info": "Italian Renaissance painter", "img": "art21.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Diego_Vel%C3%A1zquez", "name": "Diego Velázquez","info": "Spanish Golden Age painter", "img": "art22.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Titian", "name": "Titian", "info": "Italian Renaissance master","img": "art23.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/El_Greco", "name": "El Greco", "info": "Mannerism style painter","img": "art24.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Francisco_Goya", "name": "Francisco Goya","info": "Spanish Romantic painter", "img": "art25.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Marc_Chagall", "name": "Marc Chagall","info": "Modernist artist, surreal imagery", "img": "art26.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Paul_Gauguin", "name": "Paul Gauguin", "info": "Post-Impressionism painter","img": "art27.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Hokusai", "name": "Hokusai", "info": "Japanese ukiyo-e artist","img": "art28.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Jean-Michel_Basquiat", "name": "Jean-Michel Basquiat","info": "Neo-expressionism artist", "img": "art29.jpg"},
    {"wiki": "https://en.wikipedia.org/wiki/Keith_Haring", "name": "Keith Haring", "info": "Pop art / street art","img": "art30.jpg"},

]



@app.route("/")
def home():
    category = request.args.get("category", "").strip()
    search = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)

    query = Artwork.query

    if category:
        query = query.filter(Artwork.category == category)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            db.or_(
                Artwork.title.ilike(like_pattern),
                Artwork.artist.ilike(like_pattern)
            )
        )

    query = query.order_by(Artwork.id.desc())

    per_page = 6
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    artworks = pagination.items


    categories = [c[0] for c in db.session.query(Artwork.category).distinct().order_by(Artwork.category)]


    favorite_ids = set()
    if current_user.is_authenticated:
        favorite_ids = {a.id for a in current_user.favorite_artworks}

    return render_template(
        "index.html",
        artworks=artworks,
        artists=ARTISTS,
        pagination=pagination,
        categories=categories,
        selected_category=category,
        search_query=search,
        favorite_ids=favorite_ids,
    )



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data))
        new_user.create()
        flash("Registration successful! You can now log in.")
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Welcome back, " + user.username)
            return redirect("/")
        flash("Invalid username or password.")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")



@app.route("/add_artwork", methods=["GET", "POST"])
@login_required
def add_artwork():
    form = ArtworkForm()
    if form.validate_on_submit():
        new_artwork = Artwork(
            title=form.title.data,
            artist=form.artist.data,
            category=form.category.data,
            description=form.description.data,
            for_sale=form.for_sale.data,
            price=form.price.data if form.for_sale.data else None,
            user_id=current_user.id,
        )
        img = form.image.data
        if img and img.filename:
            filename = secure_filename(img.filename)
            new_artwork.image = filename
            directory = path.join(app.root_path, "static", "images", filename)
            img.save(directory)
        new_artwork.create()
        flash("Artwork added successfully!")
        return redirect("/")
    return render_template("add_artwork.html", form=form)


@app.route("/update_artwork/<int:artwork_id>", methods=["GET", "POST"])
@login_required
def update_artwork(artwork_id):
    artwork = Artwork.query.get(artwork_id)


    if not current_user.is_admin() and artwork.user_id != current_user.id:
        flash("You don't have permission to edit this artwork.")
        return redirect("/")

    form = ArtworkForm(
        title=artwork.title,
        artist=artwork.artist,
        category=artwork.category,
        description=artwork.description,
        for_sale=artwork.for_sale,
        price=artwork.price,
    )
    if form.validate_on_submit():
        artwork.title = form.title.data
        artwork.artist = form.artist.data
        artwork.category = form.category.data
        artwork.description = form.description.data
        artwork.for_sale = form.for_sale.data
        artwork.price = form.price.data if form.for_sale.data else None

        img = form.image.data
        if img and img.filename:
            filename = secure_filename(img.filename)
            directory = path.join(app.root_path, "static", "images", filename)
            img.save(directory)
            artwork.image = filename

        artwork.save()
        flash("Artwork updated successfully!")
        return redirect("/artwork/" + str(artwork_id))
    return render_template("add_artwork.html", form=form)


@app.route("/delete_artwork/<int:artwork_id>")
@login_required
def delete_artwork(artwork_id):
    artwork = Artwork.query.get(artwork_id)

    if not current_user.is_admin() and artwork.user_id != current_user.id:
        flash("You don't have permission to delete this artwork.")
        return redirect("/")

    artwork.delete()
    flash("Artwork deleted.")
    return redirect("/")


@app.route("/artwork/<int:artwork_id>", methods=["GET", "POST"])
def artwork_details(artwork_id):
    artwork = Artwork.query.get(artwork_id)

    comment_form = CommentForm()
    rating_form = RatingForm()

    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("Please log in to comment or rate.")
            return redirect(url_for("login"))

        if "submit_comment" in request.form and comment_form.validate_on_submit():
            new_comment = Comment(
                text=comment_form.text.data,
                user_id=current_user.id,
                artwork_id=artwork.id,
            )
            new_comment.create()
            flash("Comment posted!")
            return redirect(url_for("artwork_details", artwork_id=artwork.id))

        if "submit_rating" in request.form and rating_form.validate_on_submit():
            existing = Rating.query.filter_by(user_id=current_user.id, artwork_id=artwork.id).first()
            if existing:
                existing.value = int(rating_form.value.data)
                existing.save()
                flash("Rating updated!")
            else:
                new_rating = Rating(
                    value=int(rating_form.value.data),
                    user_id=current_user.id,
                    artwork_id=artwork.id,
                )
                new_rating.create()
                flash("Thanks for rating!")
            return redirect(url_for("artwork_details", artwork_id=artwork.id))

    comments = Comment.query.filter_by(artwork_id=artwork.id).order_by(Comment.created_at.desc()).all()

    user_rating = None
    is_favorited = False
    if current_user.is_authenticated:
        existing_rating = Rating.query.filter_by(user_id=current_user.id, artwork_id=artwork.id).first()
        if existing_rating:
            user_rating = existing_rating.value
        is_favorited = current_user.favorite_artworks.filter_by(id=artwork.id).first() is not None

    return render_template(
        "artwork_details.html",
        artwork=artwork,
        comments=comments,
        comment_form=comment_form,
        rating_form=rating_form,
        user_rating=user_rating,
        is_favorited=is_favorited,
    )


@app.route("/favorite/<int:artwork_id>", methods=["POST"])
@login_required
def toggle_favorite(artwork_id):
    artwork = Artwork.query.get(artwork_id)
    if not artwork:
        flash("Artwork not found.")
        return redirect("/")

    already = current_user.favorite_artworks.filter_by(id=artwork.id).first()
    if already:
        current_user.favorite_artworks.remove(artwork)
    else:
        current_user.favorite_artworks.append(artwork)
    db.session.commit()

    next_page = request.referrer or url_for("home")
    return redirect(next_page)



@app.route("/profile")
@login_required
def profile():
    my_artworks = Artwork.query.filter_by(user_id=current_user.id).order_by(Artwork.id.desc()).all()
    my_favorites = current_user.favorite_artworks.order_by(Artwork.id.desc()).all()
    return render_template(
        "profile.html",
        my_artworks=my_artworks,
        my_favorites=my_favorites,
    )



@app.route("/admin/users")
@login_required
def admin_users():
    if not current_user.is_admin():
        flash("Admin access only.")
        return redirect("/")
    users = User.query.order_by(User.id).all()
    return render_template("admin_users.html", users=users)


@app.route("/admin/users/<int:user_id>/promote")
@login_required
def promote_user(user_id):
    if not current_user.is_admin():
        flash("Admin access only.")
        return redirect("/")
    user = User.query.get(user_id)
    if user:
        user.role = "Admin"
        user.save()
        flash(f"{user.username} is now an Admin.")
    return redirect(url_for("admin_users"))


@app.route("/admin/users/<int:user_id>/demote")
@login_required
def demote_user(user_id):
    if not current_user.is_admin():
        flash("Admin access only.")
        return redirect("/")
    user = User.query.get(user_id)
    if user:
        if user.id == current_user.id:
            flash("You cannot demote yourself.")
        else:
            user.role = "Guest"
            user.save()
            flash(f"{user.username} is now a Guest.")
    return redirect(url_for("admin_users"))
