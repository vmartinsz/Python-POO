# Programação Orientada a Objetos
# AC2 POO - Tratamento de exceções
#
# Email Impacta: vitor.martins@aluno.faculdadeimpacta.com.br


def raiz_quadrada(n):
	if n >= 0:
		n = n**0.5
		return n
	else:
		raise ValueError
        
def area_retangulo(base, altura):
   if not isinstance(base, float) or not isinstance(altura, float):
        raise TypeError("Os parâmetros devem ser do tipo float.")
    
   if base < 0 or altura < 0:
        raise ValueError("Os lados do retângulo não podem ser negativos.")
      
   return base * altura

def cpf_de_sp(cpf):
    try:
        cpf_str = str(cpf)
        if len(cpf_str) < 9:
            return False
        nono_digito = cpf_str[8]
        return nono_digito == '8'
    except:
        return False

def converte_int(valor):
    try:
        return int(valor)
    except ValueError:
        return 0
    except:
        return -1

def soma_numeros(lista):

    soma = 0
    for valor in lista:
        try:
            soma += valor
        except TypeError:
            continue
    return soma

def formata_musica(dicio): 
    try:
        nome = dicio["nome"]
        artista = dicio["artista"]
        duracao = dicio["duracao"]
        return f"{nome} - {artista} ({duracao} segundos)"
    except KeyError:
        print("Erro ao consultar uma das chaves do dicionário")
    except:
        print("Erro desconhecido")

def media(notas):
     try:
          if len(notas) == 0:
               raise ZeroDivisionError
          else:
               soma = sum(notas)
               media = soma / len(notas)
               return media
     except TypeError:
          print("A lista deve conter somente números")
     except ZeroDivisionError:
          print("A lista não pode ser vazia")
     except:
          print("Erro desconhecido")               

