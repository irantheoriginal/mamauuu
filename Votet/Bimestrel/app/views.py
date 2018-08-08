# -*- coding: utf-8 -*-

from flask import g, session, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import app, lm, db
from app.models.forms import LoginForm
from app.models import tabelas
from sqlalchemy import desc
from threading import Thread, Event
import time
import psycopg2, psycopg2.extras

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@lm.user_loader
def load_user(id):
    return tabelas.Usuario.query.filter_by(id=id).first()

@main.route('/index', methods =['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index,html', form=form, posts=posts)

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():

    if request.method == 'POST':
        user = request.form['user']
        email = request.form['email']
        senha = request.form['senha']

        cadastro = tabelas.Usuario(nome=user,email=email,senha=senha)
        db.session.add(cadastro)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template('conta/cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = tabelas.Usuario.query.filter_by(email=form.email.data).first()
        if user and user.senha == form.senha.data:
            login_user(user)
            session['name'] = request.form['email']
            flash("Usuario Logado.")
            return redirect(url_for("dashboard"))
        else:
            flash("Login Invalido!")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    if request.method == "POST":

        data = time.asctime(time.localtime(time.time()))
        postar = request.form['lei']

        cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT id FROM usuario WHERE email='%s' LIMIT 1;" %session['name'])
        ds = cur.fetchone()
        for d in ds:
            print(d)
        cur.close()

        p = tabelas.Publicacao(id_user=d,data=data,conteudo=postar)
        db.session.add(p)
        db.session.commit()

    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id FROM usuario WHERE email='%s' LIMIT 1;" %session['name'])
    id_user = cur.fetchone()
    for d in id_user:
        print(d)
    cur.close()

    public = tabelas.Publicacao.query.filter_by(id_user=d).order_by(desc('id'))
    return render_template('conta/dashboard.html',publicacao=public,a=session['name'])

@app.route('/dashboard/excluir/<int:id>')
@login_required
def excluir(id):

    d = tabelas.Publicacao.query.filter_by(id=id).first()
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for('dashboard'))

poll_data = {
   'question' : x,
   'fields'   : ['Sim', 'Não']
}
filename = 'data.txt'
 
@app.route('/lei')
def Lei(method= 'POST'):
    x=input("Digite aqui sua proposta e lei")
    voe = request.args.get('question')
    leiposta = request.form['lei']
    out = open(filename, 'a')
    out.write(leiposta)
    out.close()

@app.route('/poll')
def poll():
    vote = request.args.get('field')
    out = open(filename, 'a')
    if stop_event.is_set():
        out.write(Null)
    else:
        out.write( vote + '\n' )
    out.close()

    return render_template('obgpv.html', data=poll_data)
 
@app.route('/results')
def show_results():
    votes = {}
    for f in poll_data['fields']:
        votes[f] = 0
 
    f  = open(filename, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] +=1
 
    return render_template('resultado.html', data=poll_data, votes=votes)

if __name__ == "__main__":
    app.run(debug=True)
    action_thead = Thread(target=do_actions)
    action_thead.start()
    action_thead.join(timeout=60*60)
    stop_event.set()