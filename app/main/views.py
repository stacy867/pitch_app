from flask import render_template,request,redirect,url_for,abort
from . import main
from .. import db,photos
from .forms import UpdateProfile,PitchForm
from ..models import  User,Category,Pitch,Comment
from flask_login import login_required, current_user
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

#LIKES AND DISLIKES
@main.route('/pitch/<int:id>',methods = ['GET','POST'])
def pitch(id):
    pitch =Pitch.get_pitches(id)
    
    if request.args.get("upvotes"):
        pitch.upvotes = pitch.upvotes +1
        
        db.session.add(pitch)
        db.session.commit()
        
        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
    elif request.args.get("downvotes"):
        pitch.downvotes = pitch.downvotes + 1
        
        db.session.add(pitch)
        db.session.commit()
        
        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
        

@main.route('/')
def index():
    # category = Category.query.get(id)
    categoryy=Category.get_categories()
    # pitches=Pitch.get_pitches(id)
    # comment =Comments.get_comments(id)
    # pitches = Pitch.query.filter_by(category=id).all()
    
    return render_template('index.html', category=categoryy)

#inserting a new pitch
@main.route('/categories/view_pitch/add/<int:id>', methods=['GET','POST'])
@login_required
def new_pitch(id):
    '''
    function to enter new pitches and fetch data from them
    '''
    form = PitchForm()
    category = Category.query.filter_by(id=id).first()
    title=f'welcome to pitches'
    
    if category is None:
        abort(404)
        
    if form.validate_on_submit():
        content = form.content.data
        new_pitch= Pitch(content=content,category=category.id,user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.index',id=category.id))
    return render_template('new_pitch.html', title = title, pitch_form = form, category = category)
            
#viewing a Pitch with its comments
@main.route('/categories/view_pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def viewing_pitch(id):
    '''
    a function to view inserted pitches
    '''
    print(id)
    
    pitches=Pitch.get_pitches(id)
    
    # if pitches is None:
    #     abort(404)
    comment =Comments.get_comments(id)
    return render_template('pitch.html', pitches=pitches,category_id=id)
    

