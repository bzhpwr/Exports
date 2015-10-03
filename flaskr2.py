import sqlite3, os, pprint, yaml, uuid
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

app.config.update(dict(
#    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
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
#def connect_db():
#    rv = sqlite3.connect(app.config['DATABASE'])
#    rv.row_factory = sqlite3.Row
#    return rv

def import_datas():
  f = open('./exemple.yml')
  d_folders = yaml.load(f)
  f.close()
  if not d_folders:
      d_folders = {}
  return d_folders

def write_datas(d_folders):
  with open('exemple.yml', 'w') as outfile:
        outfile.write( yaml.dump(d_folders, default_flow_style=False) )
  
@app.route('/')
def show_entries():
    l_folders = os.listdir('/usr')
    d_folders = import_datas()
    return render_template('show_entries.html', d_folders=d_folders, l_folders=l_folders)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    d_folders = import_datas()
    test = [y for x in d_folders.values() for y in x.values() if y == str(request.form['Folder'])]
    if test:
      print(test)
      flash('This folder already exist in list')
    else:
      Folder_id = uuid.uuid4()
      d_folders[str(Folder_id)] = { 'Folder':str(request.form['Folder']), 'Password':str(request.form['Password']), 'Hostnames':str(request.form['Hostnames']), 'Receivers':str(request.form['Receivers']) }
      write_datas(d_folders)
      flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/del', methods=['POST'])
def del_entry():
    if not session.get('logged_in'):
        abort(401)
    d_folders = import_datas()
    print(type(request.form['Folder']))
    if request.form['Folder'] in d_folders.keys():
      del d_folders[request.form['Folder']] 
      write_datas(d_folders)
      flash('Entry was successfully delete')
    else:
      flash('This folder not exist in list')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials'
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
