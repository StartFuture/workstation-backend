import itertools
import re
import smtplib
import email.message
import os
import logging
from datetime import datetime

import requests
from dotenv import load_dotenv

import parameters
from models.dao import DataBaseBox

def convert_cod_int(cod : str):
    cod = str(cod).strip()
    if cod.isnumeric():
        cod = int(cod)
        return cod
    else:
        return 0

def convert_str_code(value_input : str) -> str:
    value = str(value_input).strip().replace('.', '').replace('-', '')
    
    return value


def convert_str_float(value_input : str) -> float:
    value = str(value_input).strip().replace(',', '')
    try:
        value = float(value)
    except:
        logging.error(f'Error while converting value to float: {value_input}')
        value = 0.0
        
    finally:
        return value

def convert_str_int(value_input : str) -> int:
    value = str(value_input).strip().replace(',', '')
    try:
        value = int(value)
    except:
        logging.error(f'Error while converting value to int: {value_input}')
        value = 0
    finally:
        return value

def check(user):
    return bool(re.match(r"[a-zA-Z0-9\.]+@[a-z]+.[a-z]+.?b?r?", user))


def validates(email, cpf, data):
    c = 0

    if validates_cpf(cpf):
        c += 1

    if re.match(r"[a-zA-Z0-9\.]+@[a-z]+.[a-z]+.?b?r?", email):
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

    if re.match(r"[a-zA-Z0-9\.]+@[a-z]+.[a-z]+.?b?r?", email):
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


def date_conversor(input_date, input_format_date='%d/%m/%Y', output_format_date='%Y-%m-%d'):
    
    input_date = str(input_date).strip()
    input_date = datetime.strptime(input_date, input_format_date).strftime(output_format_date)
    
    return input_date

def send_email(client_email, layout_email): # should return if the email was sent
    msg = email.message.Message()
    msg['Subject'] = "Código de verificação"
    msg['From'] = parameters.USER_EMAIL
    msg['To'] = client_email
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(layout_email)

    if parameters.PASSWORD_EMAIL:
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], parameters.PASSWORD_EMAIL)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        # print('Email enviado')
        logging.info('Email enviado')
        return True
    else:
        return False
        logging.warning('Email não enviado')
    
    
def process_data_box(id_box):

    if id_box:
        dict_box = DataBaseBox.get_boxes_by_id(id_box)
        adress_box = DataBaseBox.get_address_by_id(dict_box['id_endereco'])
        if adress_box:
            dict_box_details = adress_box.copy()
            dict_box_details['id_box'] = dict_box['id_box']
            dict_box_details['nome'] = dict_box['nome']
            dict_box_details['preco_hora'] = dict_box['preco_hora']
            dict_box_details['descricao'] = dict_box['descricao']
            dict_box_details['zone'] = dict_box['zone']

        return dict_box_details
    else:
        boxes = DataBaseBox.get_boxes_all()

        list_infos_box = []
        list_box = []
        list_address = []

        if boxes:
            for dict_box in boxes:
                adress_box = DataBaseBox.get_address_by_id(dict_box['id_endereco'])
                if adress_box:

                        dict_box_details = adress_box.copy()
                        dict_box_details['id_box'] = dict_box['id_box']
                        dict_box_details['nome'] = dict_box['nome']
                        dict_box_details['preco_hora'] = dict_box['preco_hora']
                        dict_box_details['descricao'] = dict_box['descricao']
                        dict_box_details['zone'] = dict_box['zone']

                        list_box.append(dict_box_details)

        return list_box

def search_cep(cep : str) -> dict:
    cep = str(cep).strip().replace('.', '').replace('-', '')
    if len(cep) != 8 or not cep.isnumeric():
        logging.error(f'error value received: {cep}')
        raise ValueError('cep code should have 8 numeric characters')
    result = requests.get(parameters.API_CONSULT_CEP.format(cep_code=cep))
    if result.status_code == 200:
        return result.json()
    else:
        return None