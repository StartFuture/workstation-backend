import re
from flask_restful import Resource, reqparse

acceptedCreditCards = {
    "visa": r"/^4[0-9]{12}(?:[0-9]{3})?$/",
    "mastercard": r"/^5[1-5][0-9]{14}$|^2(?:2(?:2[1-9]|[3-9][0-9])|[3-6][0-9][0-9]|7(?:[01][0-9]|20))[0-9]{12}$/",
    "amex": r"/^3[47][0-9]{13}$/",
    "discover": r"/^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$/",
    "diners_club": r"/^3(?:0[0-5]|[68][0-9])[0-9]{11}$/",
    "jcb": r"/^(?:2131|1800|35[0-9]{3})[0-9]{11}$/"
};

def validate_card(card_number):
    
    count_number_of_matchs = 0
    
    for name_compaing, card_number_regex in acceptedCreditCards.items():
        if re.match(card_number, card_number_regex):
            count_number_of_matchs += 1
            name = name_compaing
        
    if count_number_of_matchs == 1:
    
        return [True, name]
    
    if count_number_of_matchs > 1 or count_number_of_matchs == 0:
        
        return [False, None] 
        
        
def validate_cvv(cvv):
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
    try:
        cvv = int(cvv)
    except Exception as error:
        return False
    else:
        cvv = str(cvv)
        if len(cvv) in {3, 4}:
            return True
        else:
            return False
            
        
def validate_name(name):
    regex_name = r"^[A-Za-z ]+$"

    return bool(re.match(regex_name, name))
    
    
def validate_due_date(date):
    regex_date = r"""
    ^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|
    (?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|
    [2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)
    ?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|
    [3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?
    :0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$
    """
    return bool(re.match(regex_date, date))
    
    
class Payments(Resource):
    
    @staticmethod
    def post():
        argumentos = reqparse.RequestParser()
        
        argumentos.add_argument('nome')
        argumentos.add_argument('num_card')
        argumentos.add_argument('cvv')
        argumentos.add_argument('data')
        
        dados = argumentos.parse_args()
        
        bool_card_number, card = validate_card(dados['num_card'])
        
        if bool_card_number:
            if validate_cvv(dados['cvv']):
                if validate_due_date(dados['data']):
                    if validate_name(dados['nome']):
                        return {
                            'msg': 'sucessfull payment',
                            'card': card
                        }
                    return {
                        'msg': 'name error'
                    }
                return {
                    'msg': 'date error'
                }
            return {
                'msg': 'cvv error'
            }
        return {
            'msg': 'number card error'
        }