import itertools
import re
import smtplib
import email.message
import os
from dotenv import load_dotenv

from models.dao import DataBaseBox

def check(user):
    return bool(re.match(r"[a-zA-Z0-9]+@[a-z]+.[a-z]+.?b?r?", user))


def validates(email, cpf, data):
    c = 0

    if validates_cpf(cpf):
        c += 1

    if re.match(r"[a-zA-Z0-9]+@[a-z]+.[a-z]+.?b?r?", email):
        c += 1

    if re.match(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", data):
        c += 1

    if c == 3:
        return True
    return False


def validates_cpf(cpf):
    if len(cpf) != 11:
        return False

    cpf = cpf.replace('.', '').replace('-', '')

    novo_cpf = cpf[:9]

    conta = sum(int(novo_cpf[p]) * c for p, c in enumerate(range(10, 1, -1)))
    conta_2 = 11 - (conta % 11)

    primeiro_digito = '0' if conta_2 > 9 else str(conta_2)
    novo_cpf += primeiro_digito

    conta = sum(int(novo_cpf[p]) * c for p, c in enumerate(range(11, 1, -1)))
    conta_2 = 11 - (conta % 11)

    segundo_digito = '0' if conta_2 > 9 else str(conta_2)
    novo_cpf += segundo_digito
    
    return novo_cpf == cpf


def validates_pj(email, cnpj, data):
    c = 0

    if validates_cnpj(cnpj):
        c += 1

    if re.match(r"[a-zA-Z0-9]+@[a-z]+.[a-z]+.?b?r?", email):
        c += 1

    if re.match(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", data):
        c += 1

    if c == 3:
        return True
    return False


def validates_cnpj(cnpj):
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj) != 14:
        return False
    new_cnpj = cnpj[:12]
    p_num = list(cnpj[:4])
    rest = list(cnpj[4:12])

    calc = sum(
        int(p_num[pos]) * num for pos, num in enumerate(range(5, 1, -1))
    )

    for pos, num in enumerate(range(9, 1, -1)):
        calc += int(rest[pos]) * num

    account = 11 - (calc % 11)

    new_cnpj += '0' if account > 9 else str(account)
    p_num = list(new_cnpj[:5])
    rest = list(new_cnpj[5:13])

    for pos, num in enumerate(range(6, 1, -1)):
        calc += int(p_num[pos]) * num

    for pos, num in enumerate(range(9, 1, -1)):
        calc += int(rest[pos]) * num

    account = 11 - (calc % 11)

    new_cnpj += '0' if account > 9 else str(account)

    return new_cnpj == cnpj


def is_cpf(user):
    return bool(re.match(r"[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}", user))


def date_conversor(start_date, final_date):
    from datetime import datetime
    start_date = datetime.strptime(start_date.replace('/','-'), '%d-%m-%Y').date()
    final_date = datetime.strptime(final_date.replace('/','-'), '%d-%m-%Y').date()
    return start_date, final_date
    

def send_email(client_email, cod):
    load_dotenv()
    senha = os.environ.get("SENHA")
    corpo_email = f"""
    <h1>Ola,</h1>
    <h1>Seu código de verificação é:</h1>
    <h2>{cod}</h2>
    """

    msg = email.message.Message()
    msg['Subject'] = "Código de verificação"
    msg['From'] = 'WorkStation.box.email@gmail.com'
    msg['To'] = client_email
    password = senha
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    if password:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')
    
    
def process_data_box():
    boxes = DataBaseBox.show_all_boxes()
    address = DataBaseBox.show_address()

    list_infos_box = []
    list_box = []
    list_address = []

    if boxes:
        for dict_box in boxes:
            list_box.append(
                {
                    "nome": dict_box['nome'],
                    "preco": dict_box['preco_hora'],
                    "descricao": dict_box['descricao'],
                    "endereco": {}
                }
            )
            list_infos_box.append(
                    {
                        "id_box": dict_box['id_box'], 
                        "id_endereco": dict_box['id_endereco']
                    }
                )

    if address:
        list_address.extend({
                    "id_endereco": dict_address['id_endereco'],
                    "cep": dict_address['cep'],
                    "rua": dict_address['rua'],
                    "numero": dict_address['numero'],
                    "complemento": dict_address['complemento'],
                    "bairro": dict_address['bairro'],
                    "cidade": dict_address['cidade'],
                    "estado": dict_address['estado']
                } for dict_address in address)
    for box in list_box:
        for info, address in itertools.product(list_infos_box, list_address):
            if info['id_endereco'] == address['id_endereco']:
                box['endereco'] = address

    return list_box

def send_password_box(client_email, senha_box):

    load_dotenv()
    senha = os.environ.get("SENHA")
    corpo_email = f"""
    <h1>Ola,</h1>
    <h1>Sua senha de acesso para a box é:</h1>
    <h2>{senha_box}</h2>
    """

    msg = email.message.Message()
    msg['Subject'] = "Senha de acesso"
    msg['From'] = 'WorkStation.box.email@gmail.com'
    msg['To'] = client_email
    password = senha
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    if password:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')