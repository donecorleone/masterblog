from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    headline = db.Column(db.String(100), nullable=False, default='Blog Post')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Blog %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_content = request.form['content']
        blog_headline = request.form.get('headline', 'Blog Post')
        new_blog = Blog(content=blog_content)
        new_blog.headline = blog_headline

        try:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding your blog'
    else:
        blogs = Blog.query.order_by(Blog.date_created).all()
        return render_template('index.html', blogs=blogs)

@app.route('/delete/<int:id>')
def delete(id):
    blog_to_delete = Blog.query.get_or_404(id)

    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting that blog'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    blog = Blog.query.get_or_404(id)
    if request.method == 'POST':
        blog.headline = request.form['headline']
        blog.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating your blog'
    else:
        return render_template('update.html', blog=blog)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
