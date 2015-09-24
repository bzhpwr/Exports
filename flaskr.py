import sqlite3, os, pprint
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

##configuration
#DATABASE = './flaskr.db'
#DEBUG = True
#SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'admin'

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))

# create our little application :)
#app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#def connect_db():
#  return sqlite3.connect(app.config['DATABASE'])

"""Connects to the specific database."""
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

#def init_db():
#  with closing(connect_db()) as db:
#    with app.open_resource('./schema.sql', mode='r') as f:
#      db.cursor().executescript(f.read())
#    db.commit()

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    l_folders = os.listdir('/usr')
    cur = g.db.execute('select Folder, Password, Hostnames, Receivers, id from entries order by id desc')
    entries = [dict(Folder=row[0], Password=row[1], Hostnames=row[2], Receivers=row[3], Fid=row[4]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries, l_folders=l_folders)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select Folder from entries')
    entries = [dict(Folder=row[0]) for row in cur.fetchall()]
    if any(d['Folder'] == request.form['Folder'] for d in entries) is not True:
      g.db.execute('insert into entries (Folder, Password, Hostnames, Receivers ) values (?, ?, ?, ?)', [request.form['Folder'], request.form['Password'], request.form['Hostnames'], request.form['Receivers']])
      g.db.commit()
      flash('New entry was successfully posted')
    else:
      flash('This folder already exist in list')
      #flash(Markup("Hello <em>World</em>!"))
    return redirect(url_for('show_entries'))

@app.route('/del', methods=['POST'])
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from entries where id=?', [request.form['Fid']])
    g.db.commit()
    flash('Entry was successfully delete')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials'
        #elif request.form['password'] != app.config['PASSWORD']:
        #    error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
  app.run()
