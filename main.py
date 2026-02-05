from logging_utils import log_evento
from validation import validar_usuario
from services import adicionar_usuario, listar_usuarios
from rules import mostrar_resumo


def obter_usuario():
    nome = input("Digite o nome: ").strip()
    idade_str = input("Digite a idade: ").strip()
    ativo_str = input("Usuário está ativo? (s/n): ").strip().lower()

    return {
        "nome": nome,
        "idade_str": idade_str,
        "ativo_str": ativo_str
    }


def main():
    usuarios = []
    log_evento("INFO", "Sistema iniciado")

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
                log_evento("WARN", f"Falha na validação: {erro}")
                continue

            adicionar_usuario(usuarios, usuario)
            log_evento("INFO", f'Usuário cadastrado: {usuario["nome"]}')
            mostrar_resumo(usuario)

        elif opcao == "2":
            listar_usuarios(usuarios)

        elif opcao == "3":
            if not usuarios:
                print("Nenhum usuário cadastrado ainda.")
                continue
            mostrar_resumo(usuarios[-1])

        elif opcao == "0":
            log_evento("INFO", "Sistema encerrado pelo usuário")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
