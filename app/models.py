from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class Role(Enum):
    CLIENTE = 'cliente'
    ATENDENTE = 'atendente'
    ADMIN = 'admin'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.CLIENTE.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # profiles (optional): Cliente/Funcionario referenciarão user_id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == Role.ADMIN.value

    def is_atendente(self):
        return self.role == Role.ATENDENTE.value

    def is_cliente(self):
        return self.role == Role.CLIENTE.value


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    nome = db.Column(db.String(120), nullable=False)
    contato = db.Column(db.String(120), nullable=True)


class Funcionario(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(80), nullable=True)


class ItemCardapio(db.Model):
    __tablename__ = 'itens_cardapio'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    categoria = db.Column(db.String(80), nullable=True)


class ComandaStatus:
    ABERTA = 'aberta'
    FECHADA = 'fechada'
    PAGA = 'paga'


class Comanda(db.Model):
    __tablename__ = 'comandas'
    id = db.Column(db.Integer, primary_key=True)  # auto-increment serve como código
    codigo = db.Column(db.Integer, unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    mesa = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default=ComandaStatus.ABERTA)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    paid_at = db.Column(db.DateTime, nullable=True)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    closed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    itens = db.relationship('ItemComanda', back_populates='comanda', cascade='all, delete-orphan')
    pagamento = db.relationship('Pagamento', uselist=False, back_populates='comanda')

    def calcular_total(self):
        return sum([item.total for item in self.itens])


class ItemComanda(db.Model):
    __tablename__ = 'itens_comanda'
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('itens_cardapio.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    comanda = db.relationship('Comanda', back_populates='itens')
    item = db.relationship('ItemCardapio')


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id'), nullable=False, unique=True)
    forma = db.Column(db.String(50), nullable=False)
    valor_recebido = db.Column(db.Numeric(10, 2), nullable=False)
    troco = db.Column(db.Numeric(10, 2), nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    comanda = db.relationship('Comanda', back_populates='pagamento')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))