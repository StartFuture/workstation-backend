from flask_restful import Resource, reqparse
from defs_workstation import process_data_box
from . import dao as Bank
        
        
class ShowListBox(Resource):
    
    def get(self):  
        return handle_data_box()

class CreateBox(Resource):
    
    def post(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument("cep_endereco")
        argumentos.add_argument("nome")
        argumentos.add_argument("preco_hora")
        argumentos.add_argument("descricao")
        argumentos.add_argument("largura")
        argumentos.add_argument("altura")
        argumentos.add_argument("comprimento")
        
        dados = argumentos.parse_args()
        
        id_address = Bank.DataBaseBox.get_id_address_by_cep(dados['cep_endereco'])
        
        try:
            Bank.DataBaseBox.add_box(
                id_address=id_address, 
                name=dados['nome'], 
                price_hour=dados['preco_hora'], 
                description=dados['descricao'], 
                width=dados['largura'], 
                heigth=dados['altura'], 
                depth=dados['comprimento']
            )
        except Exception as erros:
            return {
                "msg": "Erro de Banco de dados"
            }
        else:
            return {
                "msg": "sucessfull"
            }
        
