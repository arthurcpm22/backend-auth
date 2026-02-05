from validation import validar_usuario

def teste_nome_vazio():
    dados = {"nome": "", "idade_str": "30", "ativo_str": "s"}
    usuario, erro = validar_usuario(dados)
    assert usuario is None
    assert erro == "Nome não pode ser vazio."

def teste_idade_invalida():
    dados = {"nome": "Arthur", "idade_str": "abc", "ativo_str": "s"}
    usuario, erro = validar_usuario(dados)
    assert usuario is None
    assert erro == "Idade inválida. Digite um número inteiro."

def teste_usuario_valido():
    dados = {"nome": "Arthur", "idade_str": "30", "ativo_str": "s"}
    usuario, erro = validar_usuario(dados)
    assert erro is None
    assert usuario["idade"] == 30
    assert usuario["ativo"] is True

def rodar_testes():
    teste_nome_vazio()
    teste_idade_invalida()
    teste_usuario_valido()
    print("Todos os testes manuais passaram!")

if __name__ == "__main__":
    rodar_testes()
