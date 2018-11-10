import os
from flask import Flask, jsonify, request, make_response
from flask_restplus import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'estaeachavesecreta'
#app.config['']
jwt = JWTManager(app)
api = Api (app)
## Importante para informar os erros
jwt._set_error_handler_callbacks(api)



@api.route('/desprotegido')
class Desprotegido(Resource):
    def get(self):
        return {'message': 'Falha de segurança'}

@api.route('/protegido')
class Protegido(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return {'message': 'Parabens ' + current_user + 'pela prevenção'}

login = reqparse.RequestParser()
login.add_argument('username')
login.add_argument('password')

@api.route('/login')
class Login(Resource):
    def post(self):
        args = login.parse_args()
        if args['password'] == 'password':
            access_token = create_access_token(identity=args['username'])
            refresh_token = create_refresh_token(identity=args['username'])
            return {'message': 'Login efetuado com sucesso', 'access_token': access_token}
        return {'error': 'Senha errada'}

## Erros ###
@api.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return {'message': str(e)}, 401




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port , debug=True)