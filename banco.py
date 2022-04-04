def menu():
    contas = le_arquivo("Contas.txt")
    opcao = 0
    verifica_lista(contas)
    while (opcao != 5):
        try:
            print("""Selecione a opção desejada: 
            1 - Inclusão de conta
            2 - Alteração de saldo
            3 - Exclusão de conta 
            4 - Relatórios gerenciais
            5 - Sair do programa
            """)
            opcao = int(input("Informe a opção:"))
        except:
            print("Opção inválida! Escolha uma opção de 1 a 5.")
        if opcao == 1:
            opcao_1(contas)
            verifica_lista(contas)
        if opcao == 2:
            num_conta = valida_input_int("Informe o número da conta: ")
            contas = opcao_2(contas, num_conta)
            verifica_lista(contas)
        if opcao == 3:
            num_conta = valida_input_int("Informe o número da conta: ")
            contas = opcao_3(contas, num_conta)
            verifica_lista(contas)
        if opcao == 4:
            selecao = valida_input_int(""" Selecione uma opção: 
            [1] para listar clientes com saldo negativo
            [2] para listar clientes acima de um determinado valor
            [3] para listar todos os clientes
            Opcao: """)
            if selecao == 1:
                printa_lista(lista_saldo_negativo(contas))
            if selecao == 2:
                maior_que = valida_input_int("Informe o valor:")
                printa_lista(lista_saldo_acima(contas, maior_que))
            if selecao == 3:
                printa_lista(contas)
        if opcao == 5:
            print("Encerrando o programa...")
            escreve_arquivo("Contas.txt", contas)


def opcao_1(lista):
    nome = verifica_nome("Digite seu nome completo:")
    numero_conta = valida_input_int("Informe o número da conta: ")
    while (verifica_conta(lista=lista, num_conta=numero_conta) != False):
        print("Numero de Conta já existe")
        numero_conta = valida_input_int("Informe o número da conta: ")
    saldo = valida_input_int("Informe o seu saldo: ")
    while (valida_saldo(saldo) == False):
        saldo = valida_input_int("Informe o seu saldo: ")
    insere_conta(lista=lista, nome=nome, num_conta=numero_conta, saldo=saldo)
    return lista


def valida_input_int(texto):
    valor = 0
    int_ok = False
    while (not int_ok):
        try:
            valor = int(input(texto))
            int_ok = True
        except:
            print("Responda apenas com numeros.")
    return valor


def opcao_2(lista, num_conta):
    if verifica_conta(lista, num_conta) == False:
        print("Informe um numero de conta válido")
    else:
        menu2 = valida_input_int("Digite 1 para saque e 2 para depósito: ")
        if menu2 == 1:
            valor = valida_input_int("Digite o valor que quer Sacar: ")
            lista = debito_saldo(valor, num_conta, lista)
        if menu2 == 2:
            valor = valida_input_int("Digite o valor que quer depositar:")
            lista = credito_saldo(valor, num_conta, lista)
    return lista


def opcao_3(lista, num_conta):
    if verifica_conta(lista, num_conta) == False:
        print("Número de conta inexistente ou inválido.")
    else:
        posicao = procura_posicao_conta(lista, num_conta)
        del lista[posicao]
    return lista


def lista_saldo_acima(lista, valor):
    lista_saldo = []
    for conta in lista:
        conta_split = conta.split(",")
        if int(conta_split[2]) > valor:
            lista_saldo.append(conta)
    return lista_saldo


def lista_saldo_negativo(lista):
    lista_saldo = []
    for conta in lista:
        conta_split = conta.split(",")
        if int(conta_split[2]) < 0:
            lista_saldo.append(conta)
    return lista_saldo


def printa_lista(lista):
    for posicao in lista:
        posicao_split = posicao.split(",")
        print(
            "Nome do Titular:" + posicao_split[0] + " Numero da Conta: " + posicao_split[1] + " Saldo:" + posicao_split[
                2])


def debito_saldo(valor, num_conta, lista):
    saldo = consulta_saldo(lista, num_conta)
    saldo = int(saldo) - valor
    posicao = procura_posicao_conta(lista, num_conta)
    dados = lista[posicao].split(",")
    lista[posicao] = dados[0] + "," + dados[1] + "," + str(saldo)
    return lista


def credito_saldo(valor, num_conta, lista):
    saldo = consulta_saldo(lista, num_conta)
    saldo = int(saldo) + valor
    posicao = procura_posicao_conta(lista, num_conta)
    dados = lista[posicao].split(",")
    lista[posicao] = dados[0] + "," + dados[1] + "," + str(saldo)
    return lista


def procura_posicao_conta(lista, num_conta):
    contador = 0
    for contas in lista:
        if contas.split(",")[1] == str(num_conta):
            return contador
        else:
            contador = contador + 1
    return -1


def consulta_saldo(lista, num_conta):
    conta = pesquisa_conta_numero(lista, num_conta)
    saldo = conta.split(",")[2]
    return saldo


def valida_saldo(saldo):
    if saldo >= 0:
        return True
    return False


def pesquisa_conta_numero(lista, numero):
    for conta in lista:
        if str(numero) in conta:
            return conta
    print("NÃO ENCONTRADO")


def insere_conta(lista, num_conta, nome, saldo):
    lista.append(str(nome) + "," + str(num_conta) + "," + str(saldo) + "\n")
    return lista


def verifica_conta(lista, num_conta):
    for conta in lista:
        if str(num_conta) in conta:
            return True
    return False


def is_alpha_space(str):
    return all(char.isalpha() or char.isspace() for char in str)


def verifica_nome(msg):
    while True:
        frase = input(msg)
        if not (is_alpha_space(frase) and len(frase) >= 6):
            print("Insira seu nome e sobrenome, sem caracteres especiais ou números.")
        else:
            return frase


def le_arquivo(nome_arquivo):
    try:
        arquivo = open(nome_arquivo, 'r')
    except Exception as e:
        print("ERRO AO ABRIR O ARQUIVO")
    conteudo = arquivo.readlines()
    arquivo.close()
    return conteudo


def escreve_arquivo(nome_arquivo, contas):
    try:
        arquivo = open(nome_arquivo, 'w')
    except Exception as e:
        print("ERRO AO ABRIR O ARQUIVO")
    try:
        for linhas in contas:
            arquivo.writelines(linhas)
    except Exception as e:
        print("ERRO AO ESCREVER NO ARQUIVO")
    arquivo.close()


def verifica_lista(lista):
    lista2 = len(lista)
    if lista2 <= 0:
        print("Não há contas cadastradas!")


menu()
