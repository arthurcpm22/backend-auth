def verificar_idade(usuario):
    if usuario["idade"] >= 18:
        return f'{usuario["nome"]} é maior de idade'
    return f'{usuario["nome"]} é menor de idade'


def verificar_status(usuario):
    return "Usuário está ativo" if usuario["ativo"] else "Usuário está inativo"


def mostrar_resumo(usuario):
    print(verificar_idade(usuario))
    print(verificar_status(usuario))
    print("-" * 30)
