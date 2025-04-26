from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from flask_login import login_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
from werkzeug.security import check_password_hash
from model import User
from init import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))
        return jsonify({"mensaje": "Login exitoso"})
    
    return jsonify({"mensaje": "Credenciales inválidas"}), 401

@auth.route('/logout')
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return jsonify({"mensaje": "Sesión Cerrada"})