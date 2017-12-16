from flask import Flask
from services import product
from os import path
from services import set_resource_dir


app = Flask(__name__)
app.register_blueprint(product)


src_dir = path.dirname(path.realpath(__file__))
_resource_dir = path.join(path.dirname(src_dir), 'resources')
set_resource_dir(_resource_dir)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
