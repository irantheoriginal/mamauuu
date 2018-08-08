# -*- coding: utf-8 -*-

from app import db

class Usuario(db.Model):

	__tablename__ = 'usuario'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String)
	email = db.Column(db.String, unique=True)
	senha = db.Column(db.String)
	visto_em = db.Column(db.DateTime(), default=datetime.utcnow)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def ping(self):
		self.visto_em = datetime.utcnow()
		db.session.add(self)
		db.session.commit()

	def postagens(self):
        return Post.query.order_by(Post.timestamp.desc())

	def __init__(self,nome,telefone,email,senha):
		self.nome = nome
		self.email = email
		self.senha = senha

	def __repr__(self):
		return "<Usuario(nome='%s', email='%s')>" % (self.nome, self.email)

class Publicacao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    comments = db.relationship('Comentario', backref='title', lazy='dynamic')

    def get_comments(self):
        return Comment.query.filter_by(publicacao_id=public.id).order_by(Comment.timestamp.desc())


    def __repr__(self):
        return '<Post %r>' % (self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('publicacao.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)