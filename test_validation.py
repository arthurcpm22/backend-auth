import unittest
from validation import validar_usuario

class TestValidation(unittest.TestCase):

    def test_nome_vazio(self):
        dados = {"nome": "", "idade_str": "30", "ativo_str": "s"}
        usuario, erro = validar_usuario(dados)
        self.assertIsNone(usuario)
        self.assertEqual(erro, "Nome não pode ser vazio.")

    def test_idade_invalida(self):
        dados = {"nome": "Arthur", "idade_str": "abc", "ativo_str": "s"}
        usuario, erro = validar_usuario(dados)
        self.assertIsNone(usuario)
        self.assertEqual(erro, "Idade inválida. Digite um número inteiro.")

    def test_usuario_valido(self):
        dados = {"nome": "Arthur", "idade_str": "30", "ativo_str": "s"}
        usuario, erro = validar_usuario(dados)
        self.assertIsNone(erro)
        self.assertEqual(usuario["idade"], 30)
        self.assertTrue(usuario["ativo"])

if __name__ == "__main__":
    unittest.main()
