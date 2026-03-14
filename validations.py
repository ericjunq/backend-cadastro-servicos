import re

def validar_telefone(telefone):
    padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'

    if re.match(padrao, telefone):
        return True
    return False

import re

def validar_cpf(cpf):

    # remove tudo que não é número
    cpf = re.sub(r'\D', '', cpf)

    # precisa ter 11 dígitos
    if len(cpf) != 11:
        return False

    # bloqueia CPFs com todos números iguais
    if cpf == cpf[0] * 11:
        return False

    # cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)

    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0

    # cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)

    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0

    # verifica se os dígitos batem
    if digito1 == int(cpf[9]) and digito2 == int(cpf[10]):
        return True

    return False