import shutil
import pyodbc

#Conexão com o DB e consulta
class db_sql:
    def connection(self):
        try:
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                  'SERVER=;'
                                  'DATABASE=Desafio_SQL;'
                                  'UID=sqlserver;'
                                  'PWD=;')
        except:
            print('Não foi possível acessar o DataBase!')
        else:
            print('Acesso ao DataBase!')
            return cnxn.cursor()  # gerenciador de comandos do banco

    def validacao_cpf(self):
        global cursor
        global cliente

        cpf = input('cpf: ')
        cursor = self.connection()
        cliente = self.dados_cliente(cursor, cpf)
        if len(cliente) == 0:
            valido = False
            print('CPF não encontrado!')
        else:
            valido = True
            print('CPF encontrado com sucesso!')
        return valido

    def variaveis(self):
        try:
            pesquisa = self.validacao_cpf()
        except:
            print('Não foi possível pesquisar o CPF!')
        else:
            #cliente
            global nome_cliente
            global nacionalidade_cliente
            global est_civil_cliente
            global profissao_cliente
            global rg_cliente
            global cpf_cliente
            global endereco_cliente
            global cidade_cliente
            global estado_cliente
            #cliente
            global cnpj_agente_vendas
            global nome_agente_vendas
            global profissao_agente_vendas
            global cpf_agente_vendas
            global empresa_agente_vendas
            global endereco_agente_vendas
            global cidade_agente_vendas
            global estado_agente_vendas
            #empreendimeto
            global matricula_empreendimento
            global nome_empreendimento
            global rua_empreendimento
            global bairro_empreendimento
            global cidade_empreendimento
            global estado_empreendimento
            global valor_empreendimento

            if pesquisa == True:
                for i in cliente:
                    nome_cliente = i[0].strip()
                    nacionalidade_cliente = i[1].strip()
                    est_civil_cliente = i[2].strip()
                    profissao_cliente = i[3].strip()
                    rg_cliente = i[4].strip()
                    cpf_cliente = i[5].strip()
                    endereco_cliente = i[6].strip()
                    cidade_cliente = i[7].strip()
                    estado_cliente = i[8].strip()
                    cnpj_agente_vendas = i[9].strip()

                agente_vendas = self.dados_agente_vendas(cursor, cnpj_agente_vendas)

                for i in agente_vendas:
                    nome_agente_vendas = i[0].strip()
                    profissao_agente_vendas = i[1].strip()
                    cpf_agente_vendas = i[2].strip()
                    empresa_agente_vendas = i[3].strip()
                    endereco_agente_vendas = i[4].strip()
                    cidade_agente_vendas = i[5].strip()
                    estado_agente_vendas = i[6].strip()

                empreendimento = self.dados_empreendimento(cursor, cpf_cliente)

                for i in empreendimento:
                    matricula_empreendimento = i[0].strip()
                    nome_empreendimento = i[1].strip()
                    rua_empreendimento = i[2].strip()
                    bairro_empreendimento = i[3].strip()
                    cidade_empreendimento = i[4].strip()
                    estado_empreendimento = i[5].strip()
                    valor_empreendimento = i[6]

    def dados_cliente(self, cursor, cpf):
        try:
            cursor.execute(f"""SELECT CLIENTE.NOME, CLIENTE.NACIONALIDADE, CLIENTE.EST_CIVIL, CLIENTE.PROFISSAO,
                                CLIENTE.RG, CLIENTE.CPF, CLIENTE.ENDERECO, CLIENTE.CIDADE, CLIENTE.ESTADO, VENDA.COD_AGE
                                FROM CLIENTE INNER JOIN VENDA ON CLIENTE.CPF = VENDA.COD_CLI  WHERE COD_CLI = '{cpf}';""")
        except:
            print('Erro na pesquisa do cliente!')
        else:
            cliente = cursor.fetchall()
            return cliente

    def dados_agente_vendas(self, cursor,cnpj_agente_vendas):
        try:
            cursor.execute(f"""SELECT TOP 1 AGENTE_VENDAS.NOME, AGENTE_VENDAS.PROFISSAO, AGENTE_VENDAS.CPF,AGENTE_VENDAS.EMPRESA,
                                AGENTE_VENDAS.ENDERECO, AGENTE_VENDAS.CIDADE, AGENTE_VENDAS.ESTADO
                                FROM AGENTE_VENDAS INNER JOIN VENDA ON AGENTE_VENDAS.CNPJ = VENDA.COD_AGE
                                WHERE COD_AGE = '{cnpj_agente_vendas}';""")
        except:
            print('Erro na pesquisa do agente de vendas!')
        else:
            agente_vendas = cursor.fetchall()
            return agente_vendas

    def dados_empreendimento(self, cursor, cpf):
        try:
            cursor.execute(f"""SELECT EMPREENDIMENTOS.MATRICULA, EMPREENDIMENTOS.NOME, EMPREENDIMENTOS.RUA, EMPREENDIMENTOS.BAIRRO,
                                EMPREENDIMENTOS.CIDADE, EMPREENDIMENTOS.ESTADO, VENDA.VALOR FROM EMPREENDIMENTOS 
                                INNER JOIN VENDA ON EMPREENDIMENTOS.MATRICULA = VENDA.MATRICULA
                                WHERE VENDA.COD_CLI = '{cpf}';""")
        except:
            print('Erro na pesquisa do empreendimento!')
        else:
            empreendimento = cursor.fetchall()
            return empreendimento

#Gera o contrato em txt
class arquivo_txt:
    try:
        db_sql().variaveis()
    except:
        print('Erro na criação das variaveis!')

    def contrato(self):
        texto = f"""CONTRATO PARTICULAR DE COMPRA E VENDA\n\n
DISPOSIÇÕES COMPLETAS DO CONTRATO PARTICULAR DE COMPRA E VENDA\n
1.CLÁUSULA PRIMEIRA - DAS PARTES:\n
1.1 VENDEDOR: {nome_agente_vendas} , {profissao_agente_vendas} , portador da cédula de identidade 
CPF nº {cpf_agente_vendas}, prestador de serviço da empresa {empresa_agente_vendas} portadora do CNPJ {cnpj_agente_vendas},
residente e domiciliado à {endereco_agente_vendas} , {cidade_agente_vendas} , {estado_agente_vendas}.\n 
1.2 COMPRADOR: {nome_cliente} , {nacionalidade_cliente} , {est_civil_cliente} , {profissao_cliente} , 
portador da cédula de identidade R.G. nº {rg_cliente} e CPF nº {cpf_cliente} , residente e domiciliado à
{endereco_cliente} , {cidade_cliente} , {estado_cliente}.\n
2.CLÁUSULA SEGUNDA - DO OBJETO:\n
2.1 IMÓVEL: Localizado no {nome_empreendimento} , Matrícula nº {matricula_empreendimento} no endereço Rua {rua_empreendimento} , 
Bairro {bairro_empreendimento} - na cidade de {cidade_empreendimento}, {estado_empreendimento} .\n
3.CLÁUSULA TERCEIRA - DO PREÇO E DA FORMA DE PAGAMENTO:\n
3.1 O valor total da presente transação é de R$ {valor_empreendimento}."""
        return texto

    def criar_txt(self):
        try:
            nome_arquivo = f'{cpf_cliente}-{nome_cliente}.txt'
            caminho_arquivo = f'C:/Users/melissa.santos/OneDrive - tenda.com/Área de Trabalho/Estagio/arquivos/Desafio 4/SQL_Python/{nome_arquivo}'
            caminho_pasta = 'C:/Users/melissa.santos/OneDrive - tenda.com/Área de Trabalho/Estagio/arquivos/Desafio 4/SQL_Python/contratos'
            arquivo = open(f'{caminho_arquivo}', 'w+')
        except:
            print('Erro na criação do arquivo!')
            arquivo = False
            return arquivo
        else:
            arquivo.write(self.contrato())
            arquivo.close()
            shutil.move(caminho_arquivo, caminho_pasta)

arquivo = arquivo_txt().criar_txt()
if arquivo == False:
    print('Arquivo não pode ser gerado!')
else:
    print('Arquivo gerado com sucesso!')
