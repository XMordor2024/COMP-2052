from flask import Flask, jsonify, request, g
from flask_principal import Principal, Permission, RoleNeed, Identity, AnonymousIdentity, identity_changed, identity_loaded

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para Flask-Principal

# Inicializar Flask-Principal
principals = Principal(app)

# Definir roles como necesidades
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
viewer_permission = Permission(RoleNeed('viewer'))

# Usuarios simulados
users = {
    "admin_user": {"password": "adminpass", "roles": ["admin"]},
    "editor_user": {"password": "editorpass", "roles": ["editor"]},
    "viewer_user": {"password": "viewerpass", "roles": ["viewer"]}
}

# Cargar roles del usuario cuando se autentica
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = g.user
    if hasattr(g.user, 'roles'):
        for role in g.user.roles:
            identity.provides.add(RoleNeed(role))

# Simular login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if user and user['password'] == password:
        g.user = type('User', (object,), {'id': username, 'roles': user['roles']})
        identity_changed.send(app, identity=Identity(username))
        return jsonify({"message": f"Logged in as {username}", "roles": user['roles']})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Ruta protegida: solo admin
@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_area():
    return jsonify({"message": "Welcome to the admin area!"})

# Ruta protegida: admin o editor
@app.route('/edit')
@editor_permission.require(http_exception=403)
def edit_area():
    return jsonify({"message": "Welcome to the editor area!"})

# Ruta pública
@app.route('/public')
def public_area():
    return jsonify({"message": "This is a public endpoint, no login required."})

# Ruta protegida: cualquier rol (admin, editor, viewer)
@app.route('/dashboard')
@viewer_permission.require(http_exception=403)
def dashboard_area():
    return jsonify({"message": "Welcome to the dashboard!"})

@app.route('/logout', methods=['POST'])
def logout():
    g.user = None
    identity_changed.send(app, identity=AnonymousIdentity())
    return jsonify({"message": "Logged out successfully"})

# Error handler para permisos denegados
@app.errorhandler(403)
def forbidden(e):
    return jsonify({"message": "Access forbidden: You don't have permission for this resource."}), 403

if __name__ == '__main__':
    app.run(debug=True)
