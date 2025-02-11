def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:  # noqa: PLR2004
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = (soma * 10) % 11
        if digito == 10:  # noqa: PLR2004
            digito = 0
        if digito != int(cpf[i]):
            return False

    return True

def validar_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:  # noqa: PLR2004
        return False

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    def calcular_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        digito = soma % 11
        return '0' if digito < 2 else str(11 - digito)  # noqa: PLR2004

    if calcular_digito(cnpj, pesos1) != cnpj[12]:
        return False
    if calcular_digito(cnpj, pesos2) != cnpj[13]:
        return False

    return True


