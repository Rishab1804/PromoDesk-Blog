from flask import *
from flask_login import login_user,logout_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from datetime import datetime
app = Flask(__name__)
def test_connection():
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        app.config['SECRET_KEY']='qwertyuiopasdfghjklzxcvbnm'
        db = SQLAlchemy(app)
        login_manager = LoginManager()
        login_manager.init_app(app)


        class User(UserMixin,db.Model):
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(120), unique=True, nullable=False)
            fname = db.Column(db.String(80), nullable=False)
            lname = db.Column(db.String(120), nullable=False)
            password = db.Column(db.String(80), nullable=False)
            def __repr__(self):
                return '<User %r>' % self.email + self.password
            

        class Blog(UserMixin,db.Model):
            id = db.Column(db.Integer, primary_key=True)
            author = db.Column(db.String(120), nullable=False)
            title = db.Column(db.String(80), nullable=False)
            content = db.Column(db.String(120), nullable=False)
            date = db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)
            db.relationship('User')
            def __repr__(self):
                return '<User %r>' % self.author + self.title + self.content + self.date
        @app.route('/', methods=['GET', 'POST'])
        def index():
            blogm=Blog.query.all()
            return render_template('index.html',data=blogm)

        @app.route('/about')
        def about():
            return render_template('about.html')
        
        @app.route('/login', methods=['POST', 'GET'])
        def login():
            if request.method=='POST':
                email=request.form.get('email')
                password=request.form.get('password')
                user =User.query.filter_by(email=email).first()
                if user and password==user.password:
                    login_user(user, remember=True)
                    flash(f'Welcome back to PromoDesk Blog {email}', 'success')
                    return redirect('/')
                else:
                    flash(f'Invalid Credentials.', 'warning')
                    return redirect('/login')
            return render_template("login.html")

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                fname = request.form.get('first_name')
                lname = request.form.get('last_name')
                user=User(email=email,password=password,fname=fname,lname=lname)
                db.session.add(user)
                db.session.commit()
                flash(f'Welcome to PromoDesk Blog {email}', 'success')
                return redirect('/login')

            return render_template('register.html')
        
        @app.route('/logout')
        @login_required
        def logout():
            logout_user()
            flash('Logged Out of your Account', 'success')
            return redirect('/')
        
        @app.route('/create_blog', methods=['GET', 'POST'])
        def create_blog():
            if request.method == 'POST':
                email = request.form.get('email')
                password = request.form.get('password')
                title = request.form.get('title')
                content = request.form.get('content')
                user=User.query.filter_by(email=email).first()
                if user and user.password==password:
                    blog=Blog(author=email,title=title,content=content)
                    db.session.add(blog)
                    db.session.commit()
                    flash(f'Posted on PromoDesk Blog', 'success')
                    return redirect('/')
            return render_template("create_blog.html")
        
        @app.route('/search-blog', methods=['GET','POST'])
        def search_blog():
            if request.method == 'POST':
                searched=request.form.get("search")
                blogx=Blog.query.filter_by(title=searched) 
                return render_template("searchblog.html", data=blogx)  
            return render_template("searchblog.html")

        @app.route('/user-blog', methods=['GET','POST'])
        def user_blog():
            if request.method == 'POST':
                searched=request.form.get("search")
                blogy=Blog.query.filter_by(author=searched) 
                return render_template("blogofauthor.html", data=blogy)
            return render_template("blogofauthor.html")   
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        if __name__ == "__main__":
            db.create_all()
            app.run(debug=True)

        
test_connection()