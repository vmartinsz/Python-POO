import pytest
import re
import os.path
import excecoes as atv


class ObjetoNaoConversivelString:

	def __str__(self):
		raise Exception("Este objeto não pode ser convertido para string")


class StringNaoComparavel(str):

	def __eq__(self, outro):
		raise Exception("Esta string não pode ser comparada")
	
	def __str__(self):
		return StringNaoComparavel("")


def verifica_imports_inputs(arq="excecoes.py"):
	if os.path.exists(arq):
		with open(arq, 'r') as f:
			conteudo = f.read()
			assert "import " not in conteudo, 'Erro: o arquivo "{0}" não pode importar bibliotecas externas'.format(arq)
			assert re.search(r"input\s*[(]", conteudo) is None, 'Erro: o arquivo "{0}" não pode usar o comando input()'.format(arq)


def compara_strings(padrao, s):
	tabela = str.maketrans("áéíóúãõàêôÁÉÍÓÚÃÕÀÊÔ", "aeiouaoaeoAEIOUAOAEO")
	if re.match(padrao, s.translate(tabela)):
		return True
	else:
		return False


@pytest.mark.parametrize('n,esperado,tipo_excecao', [
	(0, 0.0, None),
	(1, 1.0, None),
	(49, 7.0, None),
	(144, 12, None),
	(-0.01, None, ValueError),
	(-1, None, ValueError),
	(-49, None, ValueError),
])
def test_raiz_quadrada(n, esperado, tipo_excecao):
	verifica_imports_inputs()
	if tipo_excecao:
		try:
			atv.raiz_quadrada(n)
		except Exception as e:
			assert type(e) == tipo_excecao, f"A função raiz_quadrada() não lançou uma exceção do tipo {tipo_excecao.__name__}"
		else:
			assert False, f"A função raiz_quadrada() não lançou uma exceção do tipo {tipo_excecao.__name__}"
	else:
		assert atv.raiz_quadrada(n) == esperado, "A função raiz_quadrada() retorna um valor diferente do esperado"


@pytest.mark.parametrize('base,altura,esperado,tipo_excecao', [
	(2.0, 2.0, 4.0, None),
	(3.0, 5.0, 15.0, None),
	(2, 2, None, TypeError),
	(2.0, 2, None, TypeError),
	(3, 5.0, None, TypeError),
	(-2.0, -5.0, None, ValueError),
	(-2.0, 5.0, None, ValueError),
	(3.0, -4.0, None, ValueError),
])
def test_area_retangulo(base, altura, esperado, tipo_excecao):
	verifica_imports_inputs()
	if tipo_excecao:
		try:
			atv.area_retangulo(base, altura)
		except Exception as e:
			assert type(e) == tipo_excecao, f"A função area_retangulo() não lançou uma exceção do tipo {tipo_excecao.__name__}"
		else:
			assert False, f"A função area_retangulo() não lançou uma exceção do tipo {tipo_excecao.__name__}"			
	else:
		assert atv.area_retangulo(base, altura) == esperado, "A função area_retangulo() retorna um valor diferente do esperado"


@pytest.mark.parametrize('cpf,esperado', [
	(11122233899, True),
	("99966677899", True),
	(90919293894, True),
	("01234567890", True),
	(1122899, False),
	("77889", False),
	(ObjetoNaoConversivelString(), False),
	(StringNaoComparavel(), False),
])
def test_cpf_de_sp(cpf, esperado):
	verifica_imports_inputs()
	try:
		assert atv.cpf_de_sp(cpf) == esperado, f"A função cpf_de_sp() retorna um valor diferente do esperado"
	except:
		raise AssertionError("A função cpf_de_sp() deve tratar todas as exceções utilizando o bloco try/except como especificado")


@pytest.mark.parametrize('valor,esperado', [
	("9", 9),
	(2.5, 2),
	(True, 1),
	(False, 0),
	("2.5", 0),
	("a", 0),
	([], -1),
	({}, -1),
])
def test_converte_int(valor, esperado):
	verifica_imports_inputs()
	try:
		assert atv.converte_int(valor) == esperado, f"A função converte_int() retorna um valor diferente do esperado"
	except:
		raise AssertionError("A função converte_int() deve tratar todas as exceções utilizando o bloco try/except como especificado")


@pytest.mark.parametrize('lista,esperado', [
	([1], 1),
	([1, 2, 3], 6),
	([1, 2, True, 3], 7),
	([1, False, 2], 3),
	(["a", "b"], 0),
	([1, "a", 4, "b", 10], 15),
	([4, [], False, "x", 50], 54),
	([1, 2, 3, 4, True, {}, 3.5], 14.5),
])
def test_soma_numeros(lista, esperado):
	verifica_imports_inputs()
	try:
		assert atv.soma_numeros(lista) == esperado, f"A função soma_numeros() retorna um valor diferente do esperado"
	except TypeError:
		raise AssertionError("A função soma_numeros() deveria tratar exceções do tipo TypeError. No entanto, uma exceção foi gerada ao chamá-la")
	except:
		raise AssertionError("A função soma_numeros() está lançando alguma exceção diferente de TypeError")


@pytest.mark.parametrize('dicio,esperado,tipo_excecao,saida_print', [
	({"nome": "Asa Branca", "artista": "Luiz Gonzaga", "duracao": 170}, "Asa Branca - Luiz Gonzaga (170 segundos)", None, ""),
	({"nome": "Chopin Ballade No. 4 (Op. 52)", "artista": "Krystian Zimerman", "duracao": 682}, "Chopin Ballade No. 4 (Op. 52) - Krystian Zimerman (682 segundos)", None, ""),
	({"nome": "Hocus Pocus", "artista": "Focus", "duracao": 278}, "Hocus Pocus - Focus (278 segundos)", None, ""),
	({"nome": "The Imperial March", "artista": "John Williams", "duracao": 182}, "The Imperial March - John Williams (182 segundos)", None, ""),
	({"nome": "Chopis centis", "artista": "Mamonas Assassinas", "duracoes": 165}, None, KeyError, "(?is)erro ao consultar uma das chaves do dicionario"),
	({"nome": "Chopin Scherzo No.2 (Op. 31)", "duracao": 661}, None, KeyError, "(?is)erro ao consultar uma das chaves do dicionario"),
	(["Isso é uma lista", "Sem artista", 175], None, TypeError, "(?is)erro desconhecido"),
	("nome", None, TypeError, "(?is)erro desconhecido"),
	
])
def test_formata_musica(dicio, esperado, tipo_excecao, saida_print, capfd):
	verifica_imports_inputs()
	if tipo_excecao:
		try:
			atv.formata_musica(dicio)
			stdout, stderr = capfd.readouterr()
		except:
			assert False, "A função formata_musica() deve tratar todas as exceções utilizando o bloco try/except como especificado"
		else:
			assert compara_strings(saida_print, stdout), f"A função formata_musica() deve imprimir a mensagem correta para exceções do tipo {tipo_excecao.__name__}"
	else:
		assert atv.formata_musica(dicio) == esperado, "A função formata_musica() retorna um valor diferente do esperado"



@pytest.mark.parametrize('lista,esperado,tipo_excecao,saida_print', [
	([6, 8, 10], 8.0, None, ""),
	(['abc', 'def'], None, TypeError, '(?is)a lista deve conter somente numeros'),
	([], None, ZeroDivisionError, '(?is)a lista nao pode ser vazia')
])
def test_media(lista, esperado, tipo_excecao, saida_print, capfd):
	verifica_imports_inputs()
	if tipo_excecao:
		try:
			atv.media(lista)
			stdout, stderr = capfd.readouterr()
		except Exception:
			assert False, "A função media() deve tratar todas as exceções utilizando o bloco try/except como especificado"
		else:
			assert compara_strings(saida_print, stdout), f"A função media() deve imprimir a mensagem correta para exceções do tipo {tipo_excecao.__name__}"
	else:
		assert atv.media(lista) == esperado, "A função media() retorna um valor diferente do esperado"


if __name__ == '__main__':
	pytest.main()

