from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class ItemCardapioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=200)])
    descricao = StringField('Descrição')
    preco = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    disponivel = BooleanField('Disponível')
    categoria = StringField('Categoria')
    submit = SubmitField('Salvar')


class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    contato = StringField('Contato')
    submit = SubmitField('Salvar')

class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('E-mail', validators=[Email(), Length(max=120)])
    full_name = StringField('Nome completo', validators=[DataRequired(), Length(max=120)])
    contato = StringField('Contato', validators=[Length(max=120)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem coincidir.')])
    submit = SubmitField('Criar conta')

class EditProfileForm(FlaskForm):
    # não permitimos editar username por simplicidade; só email/nome/contato/senha
    email = StringField('E-mail', validators=[Optional(), Email(), Length(max=120)])
    full_name = StringField('Nome completo', validators=[DataRequired(), Length(max=120)])
    contato = StringField('Contato', validators=[Optional(), Length(max=120)])
    new_password = PasswordField('Nova senha', validators=[Optional(), Length(min=6)])
    new_password2 = PasswordField('Confirmar nova senha', validators=[Optional(), EqualTo('new_password', message='As senhas devem coincidir.')])
    submit = SubmitField('Salvar alterações')