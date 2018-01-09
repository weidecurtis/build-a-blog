from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'xydkSSzkj334slkjx69al'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(240))

    def __init__(self, title, body):
        self.title = title
        self.body = body

        
@app.route('/', methods=['POST', 'GET'])
def index():

    return redirect('/blogs')


@app.route('/blogs')
def blog():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if (blog_id):
        blogs = Blog.query.get(blog_id)
        return render_template('singleblog.html', blogs=blogs)
    else:
        return render_template('blogs.html', title='Build A Blog!', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':
        title_error = ''
        body_error = ''
        blog_title = request.form['title']
        blog_body = request.form['body']

        if len(blog_title) < 1:
            title_error = 'Please fill in the title.'

        if len(blog_body) < 1:
            body_error = 'Please fill in the body.'

        if not title_error and not body_error:

            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blogs?id={0}.html'.format(new_blog.id))
        else:

            return render_template('addblog.html', title='Add Blog Entry',
            title_error=title_error, body_error=body_error)
    else:        
        return render_template('addblog.html', title='Add Blog Entry')


if __name__ == '__main__':
    app.run()
    