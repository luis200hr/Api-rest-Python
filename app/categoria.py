from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:19955777a@localhost:3306/api_pythonnew'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)

#Creación de tabla
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self,cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

#Esquema
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')

#GET 1
categoria_schema = CategoriaSchema()
#Get all
categorias_schema = CategoriaSchema(many=True)

#Creacion del get
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#GET por ID
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)

#Endpoint Post
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    newRegister=Categoria(cat_nom,cat_desp)
    db.session.add(newRegister)
    db.session.commit()
    return categoria_schema.jsonify(newRegister)

#Actualizar
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json(force=True)
    actualizarcategoria = Categoria.query.get(id)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    actualizarcategoria.cat_nom = cat_nom
    actualizarcategoria.cat_desp = cat_desp

    db.session.commit()

    return categoria_schema.jsonify(actualizarcategoria)

#DELETE
@app.route('/categoria/<id>', methods=['DELETE'])
def eliminar_categoria(id):
    delete_categoria = Categoria.query.get(id)
    db.session.delete(delete_categoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminar_categoria)

#mensaje de bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido Api'})

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)