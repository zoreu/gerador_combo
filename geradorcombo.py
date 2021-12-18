import csv
import requests
from random import randint, choice
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
csv_feminino = "https://github.com/zoreu/nomes-brasileiros-ibge/raw/master/ibge-fem-10000.csv"
csv_masculino = "https://github.com/zoreu/nomes-brasileiros-ibge/raw/master/ibge-mas-10000.csv"


def gerador_de_telefone(ddd=False, fixo=False):
    if fixo:
        tipo = ''
    else:
        tipo = '9'
    if ddd:
        numero = '+55 {0}{1}'.format(ddd, tipo)
    else:
        #numero = '+55 {0}'.format(tipo)
        numero = '{0}'.format(tipo)
    numero += str(randint(1,9))
    for n in range(7):
        numero += str(randint(0,9))
    return numero

            
def gerar_nome(url,quantidade,numero_maximo,output,telefone=False,nome_e_numero=True):
    with open(output, 'a', encoding='utf8') as f:
        with requests.Session() as s:
            headers = {'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'    
            }
            download = s.get(url,headers=headers)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            del my_list[0] #remover linha chave
            for i in range(0,quantidade):  
                random_list = choice(my_list)
                nome,regiao,freq,rank,sexo = random_list
                nome = nome.lower()
                if nome_e_numero:
                    n = randint(1, numero_maximo); #numero aleatório de 1 a numero_maximo
                    nome = nome + str(n)
                if telefone:
                    senha = gerador_de_telefone()
                    combo = '%s:%s\n'%(str(nome),str(senha))
                else:
                    combo = '%s:%s\n'%(str(nome),str(nome))
                f.write(combo)
                f.flush()
        s.close()
    f.close()


q1 = input('Gerar combo masculino ou feminino? (masculino/feminino): ')
if q1 and q1 == 'masculino' or q1 and q1 == 'feminino':
    if q1 == 'masculino':
        url = csv_masculino
    elif q1 == 'feminino':
        url = csv_feminino
    if q1:
        q2 = input('Quantidade de nomes a ser usado (Ex:1000): ') #quantidade
        if q2 and int(q2) > 0:
            quantidade = int(q2)
            q3 = input('Usar nomes e numeros? (sim/nao): ')#nome e numero
            if q3 and q3 == 'sim' or q3 and q3 == 'nao':
                if q3 == 'sim':
                    nome_e_numero = True
                elif q3 == 'nao':
                    nome_e_numero = False
                else:
                    nome_e_numero = True                    
                if nome_e_numero:
                    q4 = input('Quantidade maxima de numeros no nome? (Ex: 9999): ')#numero_maximo
                    if q4 and int(q4) > 0:
                        numero_maximo = int(q4)
                    else:
                        numero_maximo = 0
                else:
                    numero_maximo = 0
                q5 = input('Usar numeros de telefone como senha? (sim/nao): ')#telefone
                if q5 and q5 == 'sim' or q5 and q5 == 'nao':
                    if q5 == 'sim':
                        telefone = True
                    elif q5 == 'nao':
                        telefone = False
                    else:
                        telefone = False
                    q6 = input('Nome do arquivo a ser salvo? (Ex: meucombo.txt): ')#combo
                    if q6 and '.txt' in q6:
                        output = str(q6)
                        print('Gerando combo, aguarde....')
                        gerar_nome(url,quantidade,numero_maximo,output,telefone,nome_e_numero)
                        print('Combo gerado no arquivo: ',output)