from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import (
    Cliente, Funcionario, ItemCardapio, Comanda, ComandaStatus, Pagamento
)
from app.forms import ClienteForm, ItemCardapioForm
from decimal import Decimal
from datetime import datetime
from sqlalchemy.exc import IntegrityError


admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')


# decorator para restringir ações ao administrador/caixa
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Ação restrita ao administrador/caixa.', 'danger')
            return redirect(url_for('main.menu'))
        return func(*args, **kwargs)
    return wrapper


# --------- Itens do Cardápio (CRUD) ---------
@admin_bp.route('/itens')
@login_required
@admin_required
def listar_itens():
    itens = ItemCardapio.query.order_by(ItemCardapio.nome).all()
    form = ItemCardapioForm()
    return render_template('admin/items.html', itens=itens, form=form)


@admin_bp.route('/itens/novo', methods=['POST'])
@login_required
@admin_required
def criar_item():
    form = ItemCardapioForm()
    if form.validate_on_submit():
        item = ItemCardapio(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            disponivel=bool(form.disponivel.data),
            categoria=form.categoria.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Item cadastrado.', 'success')
    else:
        flash('Erro no formulário do item.', 'warning')
    return redirect(url_for('admin.listar_itens'))


@admin_bp.route('/itens/<int:item_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_item(item_id):
    item = ItemCardapio.query.get_or_404(item_id)
    form = ItemCardapioForm(obj=item)
    if request.method == 'POST':
        if form.validate_on_submit():
            item.nome = form.nome.data
            item.descricao = form.descricao.data
            item.preco = form.preco.data
            item.disponivel = bool(form.disponivel.data)
            item.categoria = form.categoria.data
            db.session.commit()
            flash('Item atualizado.', 'success')
            return redirect(url_for('admin.listar_itens'))
        else:
            flash('Erro no formulário do item.', 'warning')
    return render_template('admin/item_edit.html', form=form, item=item)


@admin_bp.route('/itens/<int:item_id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_item(item_id):
    item = ItemCardapio.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item excluído.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Não foi possível excluir o item (referências existentes).', 'danger')
    return redirect(url_for('admin.listar_itens'))


# --------- Clientes (CRUD) ---------
@admin_bp.route('/clientes')
@login_required
@admin_required
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.nome).all()
    form = ClienteForm()
    return render_template('admin/clients.html', clientes=clientes, form=form)


@admin_bp.route('/clientes/novo', methods=['POST'])
@login_required
@admin_required
def criar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(nome=form.nome.data, contato=form.contato.data)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente criado.', 'success')
    else:
        flash('Erro no formulário do cliente.', 'warning')
    return redirect(url_for('admin.listar_clientes'))


@admin_bp.route('/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = ClienteForm(obj=cliente)
    if request.method == 'POST':
        if form.validate_on_submit():
            cliente.nome = form.nome.data
            cliente.contato = form.contato.data
            db.session.commit()
            flash('Cliente atualizado.', 'success')
            return redirect(url_for('admin.listar_clientes'))
        else:
            flash('Erro no formulário do cliente.', 'warning')
    return render_template('admin/client_edit.html', cliente=cliente, form=form)


@admin_bp.route('/clientes/<int:cliente_id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído.', 'info')
    except Exception:
        db.session.rollback()
        flash('Não foi possível excluir o cliente (referências existentes).', 'danger')
    return redirect(url_for('admin.listar_clientes'))


# --------- Funcionários (CRUD simples via request.form) ---------
@admin_bp.route('/funcionarios')
@login_required
@admin_required
def listar_funcionarios():
    funcionarios = Funcionario.query.order_by(Funcionario.nome).all()
    return render_template('admin/employees.html', funcionarios=funcionarios)


@admin_bp.route('/funcionarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def criar_funcionario():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cargo = request.form.get('cargo', '').strip()
        if not nome:
            flash('Nome é obrigatório.', 'warning')
            return redirect(url_for('admin.listar_funcionarios'))
        funcionario = Funcionario(nome=nome, cargo=cargo)
        db.session.add(funcionario)
        db.session.commit()
        flash('Funcionário criado.', 'success')
        return redirect(url_for('admin.listar_funcionarios'))
    # GET -> mostrar formulário simples (pode reutilizar template de listagem com modal)
    return render_template('admin/employee_new.html')


@admin_bp.route('/funcionarios/<int:func_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_funcionario(func_id):
    funcionario = Funcionario.query.get_or_404(func_id)
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cargo = request.form.get('cargo', '').strip()
        if not nome:
            flash('Nome é obrigatório.', 'warning')
            return redirect(url_for('admin.editar_funcionario', func_id=func_id))
        funcionario.nome = nome
        funcionario.cargo = cargo
        db.session.commit()
        flash('Funcionário atualizado.', 'success')
        return redirect(url_for('admin.listar_funcionarios'))
    # GET -> renderiza formulário populado
    return render_template('admin/employee_edit.html', funcionario=funcionario)


@admin_bp.route('/funcionarios/<int:func_id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_funcionario(func_id):
    funcionario = Funcionario.query.get_or_404(func_id)
    try:
        db.session.delete(funcionario)
        db.session.commit()
        flash('Funcionário excluído.', 'info')
    except Exception:
        db.session.rollback()
        flash('Não foi possível excluir o funcionário (referências existentes).', 'danger')
    return redirect(url_for('admin.listar_funcionarios'))


# ---- Comandas (admin) ----
@admin_bp.route('/comandas')
@login_required
@admin_required
def listar_comandas_admin():
    comandas = Comanda.query.order_by(Comanda.created_at.desc()).all()
    return render_template('admin/comandas.html', comandas=comandas)


@admin_bp.route('/comandas/<int:codigo>')
@login_required
@admin_required
def visualizar_comanda_admin(codigo):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    total = comanda.calcular_total()
    return render_template('admin/comanda_view.html', comanda=comanda, total=total)


# ----- Excluir Comanda (Admin) -----
@admin_bp.route('/comanda/<int:codigo>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_comanda_admin(codigo):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    try:
        # Abrir uma transação explícita
        # Remover pagamentos relacionados (se houver)
        if comanda.pagamento:
            db.session.delete(comanda.pagamento)
            db.session.flush()  # aplica mudança no contexto antes de prosseguir

        # Remover itens da comanda (ItemComanda)
        # Se você tiver relationship configurada com cascade='all, delete-orphan', isso não é estritamente necessário,
        # mas fazemos explicitamente para evitar problemas com constraints.
        from app.models import ItemComanda
        itens = ItemComanda.query.filter_by(comanda_id=comanda.id).all()
        for ic in itens:
            db.session.delete(ic)
        db.session.flush()

        # Agora apagar a comanda
        db.session.delete(comanda)
        db.session.commit()
        flash(f'Comanda #{codigo} excluída pelo administrador.', 'info')
    except IntegrityError as ie:
        db.session.rollback()
        # Mensagem mais específica para problemas de integridade referencial
        flash('Não foi possível excluir a comanda por restrição de integridade no banco. Verifique dependências.', 'danger')
        # opcional: log do erro para debug: print(ie) ou logger.exception(ie)
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir a comanda: ' + str(e), 'danger')
    return redirect(url_for('admin.listar_comandas_admin'))


# ----- Pagamento de Comanda -----
@admin_bp.route('/comanda/<int:codigo>/pagar', methods=['POST'])
@login_required
@admin_required
def pagar_comanda(codigo):
    comanda = Comanda.query.filter_by(codigo=codigo).first_or_404()
    if comanda.status != ComandaStatus.FECHADA:
        flash('Somente comandas fechadas podem ser pagas.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    forma = request.form.get('forma')
    try:
        valor_recebido = Decimal(request.form.get('valor_recebido', '0'))
    except Exception:
        flash('Valor recebido inválido.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    total = comanda.calcular_total()
    if valor_recebido < total:
        flash('Valor recebido é insuficiente.', 'warning')
        return redirect(url_for('main.visualizar_comanda', codigo=codigo))

    troco = valor_recebido - total
    pagamento = Pagamento(comanda_id=comanda.id, forma=forma, valor_recebido=valor_recebido, troco=troco, paid_by=current_user.id)
    comanda.status = ComandaStatus.PAGA
    comanda.paid_at = datetime.utcnow()
    comanda.paid_by = current_user.id

    db.session.add(pagamento)
    db.session.commit()
    flash(f'Pagamento registrado. Troco: R$ {troco:.2f}', 'success')
    return redirect(url_for('main.visualizar_comanda', codigo=codigo))

