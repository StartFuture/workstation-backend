import logging
from flask_restful import Resource, reqparse
from defs_workstation import process_data_box, search_cep, convert_str_float, convert_str_int, convert_str_code
from . import dao as Bank
        
        
class ShowListBox(Resource):
    
    def get(self):  
        return process_data_box()

class CreateBox(Resource):
    
    def post(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument("cep_endereco", required=True)
        argumentos.add_argument("nome", required=True)
        argumentos.add_argument("preco_hora", required=True)
        argumentos.add_argument("descricao", required=True)
        argumentos.add_argument("zona", required=True)
        argumentos.add_argument("largura", required=True)
        argumentos.add_argument("altura", required=True)
        argumentos.add_argument("comprimento", required=True)
        argumentos.add_argument("numero", required=True)
        argumentos.add_argument("complemento", required=True)
        
        dados = argumentos.parse_args()

        id_address = Bank.DataBaseBox.get_id_address_by_elements(
                    cep=convert_str_code(dados['cep_endereco']),
                    num=convert_str_int(dados['numero']),
                    complement=str(dados['complemento']).strip().lower()
                    )

        # id_address = Bank.DataBaseBox.get_id_address_by_cep('00000000')

        
        if not id_address:

            data_cep = search_cep(dados['cep_endereco'])
            print(f'dados cep: {data_cep}')
            
            if data_cep:

                Bank.DataBaseBox.add_address(
                    cep=convert_str_code(dados['cep_endereco']),
                    street=data_cep['logradouro'],
                    number=convert_str_int(dados['numero']),
                    complement=str(dados['complemento']).strip().lower(),
                    district=data_cep['bairro'],
                    city=data_cep['localidade'],
                    state=data_cep['uf']
                    )


                id_address = Bank.DataBaseBox.get_id_address_by_elements(
                    cep=convert_str_code(dados['cep_endereco']),
                    num=convert_str_int(dados['numero']),
                    complement=str(dados['complemento']).strip().lower()
                    )

            else:

                Bank.DataBaseBox.add_address(cep='00000000', street='rua teste', number='00', complement='complemento', district='republica', city='são paulo', state='são paulo')
                id_address = Bank.DataBaseBox.get_id_address_by_elements(cep='00000000', num='00', complement='complemento')

        try:
            Bank.DataBaseBox.add_box(
                id_address=id_address,
                name=dados['nome'],
                price_hour=dados['preco_hora'],
                description=dados['descricao'],
                zone=dados['zona'],
                width=convert_str_float(dados['largura']),
                heigth=convert_str_float(dados['altura']),
                depth=convert_str_float(dados['comprimento'])
            )
        except Exception as erros:
            logging.error(erros)
            return {
                "msg": "Database Error",
            }, 400
        else:
            return {
                "msg": "sucessfull"
            }, 200
        
