import os
import shutil

# Lista dos diretórios que terão seu conteúdo esvaziado.
# O script assume que estas pastas estão no mesmo local que ele.
diretorios_alvo = ["ACs", "FQs", "PHs", "RMSs"]

# Obtém o caminho do diretório atual.
caminho_base = os.getcwd()

# Itera sobre cada nome de diretório na lista.
for nome_dir in diretorios_alvo:
    caminho_dir = os.path.join(caminho_base, nome_dir)

    # Verifica se o caminho corresponde a um diretório existente.
    if os.path.isdir(caminho_dir):
        print(f"Limpando o conteúdo de: {caminho_dir}")

        # Itera sobre todos os itens (arquivos e subpastas) dentro do diretório.
        for item in os.listdir(caminho_dir):
            caminho_item = os.path.join(caminho_dir, item)
            
            try:
                # Se for um arquivo ou link, remove.
                if os.path.isfile(caminho_item) or os.path.islink(caminho_item):
                    os.unlink(caminho_item)
                # Se for uma pasta, remove a pasta e todo o seu conteúdo.
                elif os.path.isdir(caminho_item):
                    shutil.rmtree(caminho_item)
                
                print(f"  - Excluído: {caminho_item}")

            except Exception as e:
                print(f"Erro ao excluir {caminho_item}: {e}")
    else:
        print(f"Diretório não encontrado: {caminho_dir}")

print("\nProcesso concluído.")