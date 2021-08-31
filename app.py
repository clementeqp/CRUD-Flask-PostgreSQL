from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app=Flask(__name__)

# conexion bd postgre

USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'

FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}:5433/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI']=FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Iniciamos el objeto al separar los archivos lo hacemos de otra forma
#db = SQLAlchemy(app)
db.init_app(app)



#configurar flask-migrate

migrate=Migrate()
migrate.init_app(app, db)

# Configurar wtf formularios
app.config['SECRET_KEY']='llave_secreta'








@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    #Listar personas
    #personas=Persona.query.all()
    #mantener el orden por id si no el ultimo modificado es el ultimo
    personas=Persona.query.order_by('id')

    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver(id):
    #Recuperar persona por id
    #persona = Persona.query.get(id)
    persona = Persona.query.get_or_404(id)
    return render_template('detalle.html', persona=persona)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona=Persona()
    personaForm = PersonaForm(obj=persona)

    if request.method=='POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Insertar: {persona}')
            #Insertar registro

            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template(('agregar.html'), forma = personaForm)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona = Persona.query.get_or_404(id)
    personaForm = PersonaForm(obj=persona)
    if request.method=='POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            #No hay que hacer update o add
            db.session.commit()
            return redirect(url_for('inicio'))

    return render_template('editar.html', forma = personaForm)


@app.route('/borrar/<int:id>')
def borrar(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))