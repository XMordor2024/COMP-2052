from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.models import db, User, Role
from flask_login import login_user, logout_user, login_required

# Blueprint de autenticación: gestiona login, registro y logout
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Inicia sesión de un usuario existente si las credenciales son válidas.
    """
    form = LoginForm()

    # Procesamiento del formulario si es enviado correctamente
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Verifica si el usuario existe y la contraseña es válida
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('ticket.dashboard'))  # Redirige al dashboard de tickets

        # Mensaje si las credenciales no son válidas
        flash('Credenciales inválidas', 'danger')    

    # Renderiza el formulario de login
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registra un nuevo usuario y lo asocia por defecto al rol "User".
    """    
    form = RegisterForm()
    
    # Procesa el formulario si fue enviado correctamente
    if form.validate_on_submit():
        # Buscar el rol seleccionado
            role = Role.query.filter_by(name=form.role.data).first()
            if not role:
                flash('Rol inválido seleccionado', 'danger')
            return redirect(url_for('auth.register'))

        # Crea el usuario con datos del formulario
    user = User(
        username=form.username.data,
        email=form.email.data,
        role=role
        )
    user.set_password(form.password.data)

    # Guarda en la base de datos
    db.session.add(user)
    db.session.commit()

    # Muestra mensaje de éxito
    flash('User registered successfully.')
    return redirect(url_for('auth.login'))
    
    # Renderiza el formulario de registro
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))