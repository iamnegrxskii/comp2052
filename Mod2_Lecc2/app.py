from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'  # Necessary to handle forms and flash messages

# Custom error messages
ERROR_MESSAGES = {
    'nombre': {
        'required': "El nombre es obligatorio.",
        'min_length': "El nombre debe tener al menos 3 caracteres."
    },
    'correo': {
        'required': "El correo es obligatorio.",
        'invalid': "Por favor, ingresa un correo válido."
    },
    'contraseña': {
        'required': "La contraseña es obligatoria.",
        'min_length': "La contraseña debe tener al menos 6 caracteres.",
        'match': "Las contraseñas deben coincidir."
    }
}

# User registration form
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message=ERROR_MESSAGES['nombre']['required']),
        Length(min=3, message=ERROR_MESSAGES['nombre']['min_length'])
    ])
    correo = StringField('Correo', validators=[
        DataRequired(message=ERROR_MESSAGES['correo']['required']),
        Email(message=ERROR_MESSAGES['correo']['invalid'])
    ])
    contraseña = PasswordField('Contraseña', validators=[
        DataRequired(message=ERROR_MESSAGES['contraseña']['required']),
        Length(min=6, message=ERROR_MESSAGES['contraseña']['min_length'])
    ])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message=ERROR_MESSAGES['contraseña']['required']),
        EqualTo('contraseña', message=ERROR_MESSAGES['contraseña']['match'])
    ])
    enviar = SubmitField('Registrar')

@app.route('/', methods=['GET', 'POST'])
def registrar_usuario():
    """
    Handles user registration: displays the registration form and processes user input.
    """
    form = RegistroForm()
    if form.validate_on_submit():
        # Simulating successful registration with flash messages
        flash(f"Usuario {form.nombre.data} registrado correctamente.", "success")
        return redirect('/')
    return render_template('registros.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error handler for invalid routes.
    """
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)