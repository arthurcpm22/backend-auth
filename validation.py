def validar_usuario(dados):
    nome = dados["nome"]
    if not nome:
        return None, "Nome não pode ser vazio."

    try:
        idade = int(dados["idade_str"])
    except ValueError:
        return None, "Idade inválida. Digite um número inteiro."

    if idade < 0 or idade > 120:
        return None, "Idade fora do intervalo esperado (0–120)."

    ativo_str = dados["ativo_str"]
    if ativo_str not in ("s", "n"):
        return None, 'Campo "ativo" inválido. Use "s" ou "n".'

    usuario = {
        "nome": nome,
        "idade": idade,
        "ativo": ativo_str == "s"
    }

    return usuario, None
