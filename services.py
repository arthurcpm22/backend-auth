def adicionar_usuario(usuarios, usuario):
    usuarios.append(usuario)


def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for i, usuario in enumerate(usuarios, start=1):
        print(f"[{i}] {usuario['nome']} | idade={usuario['idade']} | ativo={usuario['ativo']}")
