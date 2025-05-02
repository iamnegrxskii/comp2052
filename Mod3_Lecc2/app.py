from flask import Flask, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuramos LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configuramos Principal
principals = Principal(app)

# Definimos permisos
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id, username, roles):
        self.id = id
        self.username = username
        self.roles = roles

# Datos de ejemplo (usuarios y sus roles)
users = {
    "juan": User(1, "juan", roles=["user"]),
    "maria": User(2, "maria", roles=["admin", "user"])
}

# Cargar usuario
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

# Asignar roles al identity
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role))

# Ruta de login
@app.route("/login/<username>")
def login(username):
    user = users.get(username)
    if user:
        login_user(user)
        # Actualizar la identidad
        identity_changed.send(app, identity=Identity(user.id))
        return f"Bienvenido {current_user.username}!"
    return "Usuario no encontrado", 404

# Ruta de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return "Sesión cerrada"

# Dashboard general
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hola, {current_user.username}! Bienvenido a tu panel."

# Página solo para usuarios normales
@app.route("/user")
@login_required
@user_permission.require(http_exception=403)
def user_page():
    return f"Hola, {current_user.username}. Esta es la página de usuarios."

# Página solo para admins
@app.route("/admin")
@login_required
@admin_permission.require(http_exception=403)
def admin_page():
    return f"Hola, {current_user.username}. Esta es la página de administradores."

if __name__ == "__main__":
    app.run(debug=True)