from ast import main
from flask import Flask, jsonify
from flask_login import current_user, login_required


@main.route('/')
def index():
    return jsonify({"mensaje": "Bienvenido a la aplicación de roles y permisos"})


@main.route('/perfil')
@login_required
def perfil():
    return jsonify({
        "usuario": current_user.username,
        "rol": current_user.role.name
    })
    
@main.route('/admin-panel')
@login_required
@admin_permission.require(http_exception=403)
def admin_panel():
    return jsonify({
        "mensaje": "Bienvenido al panel de administración."
    })
    
@main.route('/zona-usuario')
@login_required
@user_permission.require(http_exception=403)
def zona_usuario():
    return jsonify({
        "mensaje": "Bienvenido a la zona del usuario."
    })