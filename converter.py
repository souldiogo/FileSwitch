from pacote_convert import converter_arquivo, encontrar_arquivo

if __name__ == "__main__":
    # Exibir o cabeçalho do programa
    print("===== Bem-vindo ao Super Conversor! =====")
    print("   Formatos suportados para conversão\n")

    # Exibir os formatos suportados 
    colunas = [
        ["Imagems", "Documentos Word", "PDF"],
        ["jpg",           "doc",         "pdf"],
        ["jpeg",          "docx",         ""],
        ["png",             "",           ""],
        ["bmp",             "",           ""],
        ["gif",             "",           ""]
    ]
    for linha in colunas:
        print("   {:<10} {:<18} {:<10}".format(*linha))
    print("\nDigite 'sair' a qualquer momento para encerrar.\n")

    # Loop principal do programa
    while True:
        arquivo = input("Nome do arquivo: ")
        if arquivo.strip().lower() == "sair":
            print("Programa encerrado.")
            break

        caminho = encontrar_arquivo(arquivo)
        if not caminho:
            print("Arquivo não encontrado. Veja se o nome do arquivo está correto.")
            continue

        formato = input("Para qual formato deseja converter: ").strip()
        if formato.lower() == "sair":
            print("Programa encerrado.")
            break
        
        #Realiza a conversão do arquivo
        resultado = converter_arquivo(caminho, formato)
        print(resultado)
        input(f"Precione Enter para continuar...\n")
