from flask_restful import Resource, reqparse

from . import dao as Bank


class Create_adress(Resource):
    
    def post(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument("cep")
        argumentos.add_argument("rua")
        argumentos.add_argument("numero")
        argumentos.add_argument("complemento")
        argumentos.add_argument("bairro")
        argumentos.add_argument("cidade")
        argumentos.add_argument("estado")
        
        dados = argumentos.parse_args()

        Bank.DataBaseBox.add_address(street=dados['rua'],
        cep=dados['cep'], city=dados['cidade'],
        complement=dados['complemento'],
        number=dados['numero'],
        state=dados['estado'],
        district=dados['bairro'])

        return{
            'msg': 'sucess'
        }