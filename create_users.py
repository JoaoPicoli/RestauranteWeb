# reset_password.py
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

users_and_passwords = {
    'euamotwinks': 'xamueldiva',
    'atendente1': 'novaSenhaAtendente123',
    'cliente1': 'novaSenhaCliente123',
}

with app.app_context():
    for username, new_pass in users_and_passwords.items():
        u = User.query.filter_by(username=username).first()
        if not u:
            print("Usuário não encontrado:", username)
            continue
        u.password_hash = generate_password_hash(new_pass)
        db.session.commit()
        print(f"Senha atualizada para {username}")
