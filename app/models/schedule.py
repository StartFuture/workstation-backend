from flask_restful import Resource, reqparse
from . import dao as Bank


class GenerateSchedule(Resource):
    
    def post(self):
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('data_inicio')
        argumentos.add_argument('hora_inicio')
        argumentos.add_argument('hora_fim')
        argumentos.add_argument('data_fim')
        
        dados = argumentos.parse_args()
        
        valido = 
    
class ShowSchedule(Resource):
    
    def get(self):
        pass
    
class DeleteSchedule(Resource):
    
    def delete(self):
        pass
    
class UpdateSchedule(Resource):
    
    def update(self):
        pass
    
