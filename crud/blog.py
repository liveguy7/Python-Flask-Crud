from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from crud.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
  

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, 'id')
            )
            db.commit()
            return redirect(url_for('blog.get_post'))

    return render_template('blog/create.html')


@bp.route('/postsX')
def get_post():
  db = get_db()
  posts = db.execute(
      'SELECT * from user, post',
  ).fetchall()
  return render_template('blog/postsX.html', posts=posts)




@bp.route('/contact')
def contact():
  return render_template('blog/contact.html')

