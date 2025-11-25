from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.models import ItemCardapio, Comanda, ItemComanda, Cliente, ComandaStatus
from decimal import Decimal
from datetime import datetime
import os
from urllib.parse import quote_plus
from app.forms import RegisterForm, EditProfileForm
from app.models import User, Cliente, Role
from flask_login import login_user
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo, Optional

main_bp = Blueprint('main', __name__, template_folder='templates')

# helper: lê o limite de comandas abertas por cliente da config/env
def get_max_open_comandas_per_client():
    try:
        return int(os.environ.get('MAX_OPEN_COMANDAS_PER_CLIENT', current_app.config.get('MAX_OPEN_COMANDAS_PER_CLIENT', 3)))
    except Exception:
        return 3


@main_bp.route('/')
def index():
    return redirect(url_for('main.menu'))


@main_bp.route('/menu')
@login_required
def menu():
    categoria = request.args.get('categoria')
    query = ItemCardapio.query
    if categoria:
        query = query.filter_by(categoria=categoria)
    itens = query.order_by(ItemCardapio.nome).all()
    categorias = db.session.query(ItemCardapio.categoria).distinct().all()
    categorias = [c[0] for c in categorias if c[0]]
    return render_template('menu.html', itens=itens, categorias=categorias)


@main_bp.route('/minhas-comandas')
@login_required
def minhas_comandas():
    # Clientes veem suas comandas, atendentes/adm veem todas (ou filtram)
    if current_user.is_cliente():
        cliente = Cliente.query.filter_by(user_id=current_user.id).first()
        if not cliente:
            flash('Perfil de cliente não encontrado.', 'warning')
            return redirect(url_for('main.menu'))
        comandas = Comanda.query.filter_by(cliente_id=cliente.id).order_by(Comanda.created_at.desc()).all()
    else:
        comandas = Comanda.query.order_by(Comanda.created_at.desc()).limit(50).all()
    return render_template('minhas_comandas.html', comandas=comandas)


@main_bp.route('/comanda/novo', methods=['GET'])
@login_required
def nova_comanda():
    cliente_id = None
    if current_user.is_cliente():
        cliente = Cliente.query.filter_by(user_id=current_user.id).first()
        if not cliente:
            flash('Perfil de cliente não encontrado.', 'warning')
            return redirect(url_for('main.menu'))
        cliente_id = cliente.id

        # verifica limite de comandas abertas por cliente
        max_allowed = get_max_open_comandas_per_client()
        open_count = Comanda.query.filter_by(cliente_id=cliente.id, status=ComandaStatus.ABERTA).count()
        if open_count >= max_allowed:
            flash(f'Você já tem {open_count} comandas abertas. Limite por cliente: {max_allowed}.', 'warning')
            return redirect(url_for('main.minhas_comandas'))

    max_codigo = db.session.query(db.func.max(Comanda.codigo)).scalar() or 0
    codigo = int(max_codigo) + 1

    comanda = Comanda(codigo=codigo, cliente_id=cliente_id, created_by=current_user.id)
    db.session.add(comanda)
    db.session.commit()
    flash(f'Comanda {comanda.codigo} criada.', 'success')
    return redirect(url_for('main.visualizar_comanda', codigo=comanda.codigo))


# ---------------------
# novo endpoint: adiciona item diretamente à comanda aberta do cliente (cria se necessário)
@main_bp.route('/comanda/adicionar-por-cliente', methods=['POST'])
@login_required
def adicionar_por_cliente():
    # só faz sentido para usuários logados; pega item_id e opcional quantidade
    try:
        item_id = int(request.form.get('item_id'))
        quantidade = int(request.form.get('quantidade', 1))
    except (TypeError, ValueError):
        flash('Dados inválidos.', 'warning')
        return redirect(url_for('main.menu'))

    item = ItemCardapio.query.get(item_id)
    if not item or not item.disponivel:
        flash('Item indisponível.', 'warning')
        return redirect(url_for('main.menu'))
    if quantidade <= 0:
        flash('Quantidade inválida.', 'warning')
        return redirect(url_for('main.menu'))

    # só clientes têm comandas vinculadas a cliente_id.
    cliente_id = None
    if current_user.is_cliente():
        cliente = Cliente.query.filter_by(user_id=current_user.id).first()
        if not cliente:
            flash('Perfil de cliente não encontrado.', 'warning')
            return redirect(url_for('main.menu'))
        cliente_id = cliente.id

        # procura por comanda aberta desse cliente
        comanda = Comanda.query.filter_by(cliente_id=cliente.id, status=ComandaStatus.ABERTA).order_by(Comanda.created_at.desc()).first()
        if not comanda:
            # verifica limite antes de criar
            max_allowed = get_max_open_comandas_per_client()
            open_count = Comanda.query.filter_by(cliente_id=cliente.id, status=ComandaStatus.ABERTA).count()
            if open_count >= max_allowed:
                flash(f'Você alcançou o limite de {max_allowed} comandas abertas.', 'warning')
                return redirect(url_for('main.minhas_comandas'))

            # cria nova comanda para o cliente
            max_codigo = db.session.query(db.func.max(Comanda.codigo)).scalar() or 0
            codigo = int(max_codigo) + 1
            comanda = Comanda(codigo=codigo, cliente_id=cliente.id, created_by=current_user.id)
            db.session.add(comanda)
            db.session.commit()
            flash(f'Comanda {comanda.codigo} criada automaticamente.', 'info')
    else:
        # se não for cliente (ex.: atendente adicionando via botão), obrigue selecionar/indicar comanda
        flash('Ação disponível apenas para clientes autenticados via botão "Adicionar à comanda".', 'warning')
        return redirect(url_for('main.menu'))

    # agora adiciona o item na comanda encontrada/criada
    preco_unit = item.preco
    total_item = Decimal(preco_unit) * quantidade
    ic = ItemComanda(comanda_id=comanda.id, item_id=item.id, quantidade=quantidade, preco_unitario=preco_unit, total=total_item)
    db.session.add(ic)
    db.session.commit()
    flash(f'Item "{item.nome}" adicionado à comanda #{comanda.codigo}.', 'success')
    return redirect(url_for('main.visualizar_comanda', codigo=comanda.codigo))


# ---------------------

@main_bp.route('/comanda/<int:codigo>')
@login_required
def visualizar_comanda(codigo):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    total = comanda.calcular_total()
    itens_disponiveis = ItemCardapio.query.filter_by(disponivel=True).order_by(ItemCardapio.nome).all()
    return render_template('comanda.html', comanda=comanda, total=total, itens_disponiveis=itens_disponiveis)


@main_bp.route('/comanda/<int:codigo>/adicionar', methods=['POST'])
@login_required
def adicionar_item(codigo):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    # Edição permitida se aberta ou se usuário admin
    if comanda.status != ComandaStatus.ABERTA and not current_user.is_admin():
        flash('Somente administrador pode editar comandas fechadas.', 'danger')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    try:
        item_id = int(request.form.get('item_id'))
        quantidade = int(request.form.get('quantidade', 1))
    except (TypeError, ValueError):
        flash('Dados inválidos.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    item = ItemCardapio.query.get(item_id)
    if not item or not item.disponivel:
        flash('Item indisponível.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))
    if quantidade <= 0:
        flash('Quantidade inválida.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    preco_unit = item.preco
    total_item = Decimal(preco_unit) * quantidade

    ic = ItemComanda(comanda_id=comanda.id, item_id=item.id, quantidade=quantidade, preco_unitario=preco_unit, total=total_item)
    db.session.add(ic)
    db.session.commit()
    flash('Item adicionado à comanda.', 'success')
    return redirect(url_for('main.visualizar_comanda', codigo=codigo))


@main_bp.route('/comanda/<int:codigo>/remover/<int:itemcomanda_id>', methods=['POST'])
@login_required
def remover_item(codigo, itemcomanda_id):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    ic = ItemComanda.query.get_or_404(itemcomanda_id)
    if ic.comanda_id != comanda.id:
        abort(403)

    if comanda.status != ComandaStatus.ABERTA and not current_user.is_admin():
        flash('Somente administrador pode editar comandas fechadas.', 'danger')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    db.session.delete(ic)
    db.session.commit()
    flash('Item removido.', 'info')
    return redirect(url_for('main.visualizar_comanda', codigo=codigo))


@main_bp.route('/comanda/<int:codigo>/fechar', methods=['POST'])
@login_required
def fechar_comanda(codigo):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    if not (current_user.is_atendente() or current_user.is_admin()):
        flash('Permissão negada para fechar comanda.', 'danger')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    if comanda.status != ComandaStatus.ABERTA:
        flash('Somente comandas abertas podem ser fechadas.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    if len(comanda.itens) == 0:
        flash('Não é possível fechar comanda vazia.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    comanda.status = ComandaStatus.FECHADA
    comanda.closed_at = datetime.utcnow()
    comanda.closed_by = current_user.id
    db.session.commit()
    flash('Comanda fechada com sucesso.', 'success')
    return redirect(url_for('main.visualizar_comanda', codigo=codigo))

# rota de registro (pública)
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    # redireciona se já estiver logado
    if current_user.is_authenticated:
        flash('Você já está logado.', 'info')
        return redirect(url_for('main.menu'))

    form = RegisterForm()
    if form.validate_on_submit():
        # valida username único
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            flash('Nome de usuário já existe. Escolha outro.', 'warning')
            return render_template('register.html', form=form)

        # cria usuário
        user = User(username=form.username.data, email=form.email.data, role=Role.CLIENTE.value)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  # commit para gerar user.id

        # cria perfil Cliente vinculado
        cliente = Cliente(user_id=user.id, nome=form.full_name.data, contato=form.contato.data)
        db.session.add(cliente)
        db.session.commit()

        # loga o usuário automaticamente (opcional)
        login_user(user)

        flash('Conta criada com sucesso. Bem-vindo!', 'success')
        return redirect(url_for('main.menu'))

    return render_template('register.html', form=form)
@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Página de edição do perfil do cliente (nome, contato, email, senha opcional).
    Se o usuário não tem um perfil Cliente, cria um automaticamente.
    """
    form = EditProfileForm()

    # garante que exista o perfil Cliente vinculado (se for cliente)
    cliente = Cliente.query.filter_by(user_id=current_user.id).first()
    if not cliente:
        # se não existir, cria um cliente com nome vazio (ou usa username)
        cliente = Cliente(user_id=current_user.id, nome=getattr(current_user, 'username', ''))
        db.session.add(cliente)
        db.session.commit()

    if request.method == 'GET':
        # popular o form com dados atuais
        form.email.data = current_user.email
        form.full_name.data = cliente.nome
        form.contato.data = cliente.contato

    if form.validate_on_submit():
        # checar email único se alterou
        new_email = form.email.data.strip() if form.email.data else None
        if new_email and new_email != current_user.email:
            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != current_user.id:
                flash('E-mail já está em uso por outro usuário.', 'warning')
                return render_template('profile.html', form=form)

        # aplicar alterações
        cliente.nome = form.full_name.data.strip()
        cliente.contato = form.contato.data.strip() if form.contato.data else None
        current_user.email = new_email

        # tratar alteração de senha (opcional)
        new_pass = form.new_password.data
        if new_pass:
            current_user.set_password(new_pass)

        db.session.commit()
        flash('Perfil atualizado com sucesso.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('profile.html', form=form)
