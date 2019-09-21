from flask import render_template,request,redirect,url_for,abort
from . import main
from .. import db,photos
from .forms import UpdateProfile
from ..models import  User,Category
from flask_login import login_required
from flask_login import UserMixin

# @main.route('/')
# def index():
    
#     '''
#     View root page function that returns the index page and its data
#     '''

    
#     title = 'Home - Welcome to The pitch website'
#     category = Category.get_categories()



    
    # return render_template('index.html', title = title ,category= category)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.update_profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/categories/<int:id>')
def index(id):
    # category = Category.query.get(id)
    categoryy=Category.get_categories()
    # pitches = Pitch.query.filter_by(category=id).all()
    
    return render_template('index.html', category=categoryy)

    

