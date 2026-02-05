def verificar_idade(usuario):
    if usuario["idade"] >= 18:
        return f'{usuario["nome"]} é maior de idade'
    return f'{usuario["nome"]} é menor de idade'


def verificar_status(usuario):
    return "Usuário está ativo" if usuario["ativo"] else "Usuário está inativo"


# --- "Controller": entrada de dados (simulando request) ---
def obter_usuario():
    nome = input("Digite o nome: ").strip()
    idade_str = input("Digite a idade: ").strip()
    ativo_str = input("Usuário está ativo? (s/n): ").strip().lower()

    return {
        "nome": nome,
        "idade_str": idade_str,
        "ativo_str": ativo_str
    }


# --- "Validator": validação e normalização ---
def validar_usuario(dados):
    # validar nome
    nome = dados["nome"]
    if not nome:
        return None, "Nome não pode ser vazio."

    # validar idade
    try:
        idade = int(dados["idade_str"])
    except ValueError:
        return None, "Idade inválida. Digite um número inteiro."

    if idade < 0 or idade > 120:
        return None, "Idade fora do intervalo esperado (0–120)."

    # validar ativo
    ativo_str = dados["ativo_str"]
    if ativo_str not in ("s", "n"):
        return None, 'Campo "ativo" inválido. Use "s" ou "n".'

    ativo = ativo_str == "s"

    usuario = {"nome": nome, "idade": idade, "ativo": ativo}
    return usuario, None


# --- "Service": operação de negócio ---
def adicionar_usuario(usuarios, usuario):
    usuarios.append(usuario)


def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for i, usuario in enumerate(usuarios, start=1):
        print(f"[{i}] {usuario['nome']} | idade={usuario['idade']} | ativo={usuario['ativo']}")


def mostrar_resumo(usuario):
    print(verificar_idade(usuario))
    print(verificar_status(usuario))
    print("-" * 30)


def main():
    usuarios = []

    while True:
        print("\n=== MENU ===")
        print("1) Cadastrar usuário")
        print("2) Listar usuários")
        print("3) Mostrar resumo do último usuário")
        print("0) Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            dados = obter_usuario()
            usuario, erro = validar_usuario(dados)

            if erro:
                print("Erro:", erro)
                continue

            adicionar_usuario(usuarios, usuario)
            print("Usuário cadastrado com sucesso.")
            mostrar_resumo(usuario)

        elif opcao == "2":
            listar_usuarios(usuarios)

        elif opcao == "3":
            if not usuarios:
                print("Nenhum usuário cadastrado ainda.")
                continue
            mostrar_resumo(usuarios[-1])

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()


def main():
    usuario = obter_usuario()

    if usuario is None:
        print("Erro ao criar usuário.")
        return

    verificar_idade(usuario["nome"], usuario["idade"])
    verificar_status(usuario["ativo"])


if __name__ == "__main__":
    main()

