import os
import pdf2docx
import logging
from PIL import Image
import sys

#Desativando mensagens de log do comtypes do termnial
logging.getLogger("comtypes").setLevel(logging.CRITICAL)

# Função para encontrar o caminho do arquivo infromado
def encontrar_arquivo(nome_arquivo):
    # Se o usúario informar um caminho absoluto e o arquivo existir
    if os.path.isabs(nome_arquivo) and os.path.exists(nome_arquivo) and os.path.isfile(nome_arquivo):
        return nome_arquivo
    
    # Define o diretório base dependendo se está rodando como script ou executável
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Diretórios padrão do sistema, porém, usa-se diretório completo se estiver no Documents(Documentos)
    documentos_pt = os.path.join(os.path.expanduser("~"), "Documentos")
    documents_en = os.path.join(os.path.expanduser("~"), "Documents")

    diretorios = [
        base_dir,
        os.getcwd(),
        os.path.expanduser("~/Downloads"),
        documentos_pt,
        documents_en
    ]
    
    # Adiciona o diretório do executável (Caso esteja rodando como um exe)
    if getattr(sys, '_MEIPASS', False):
        diretorios.insert(0, sys._MEIPASS)
        
    # Procura o arquivo nos diretórios listados
    for diretorio in diretorios:
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        if os.path.exists(caminho_arquivo):
            return caminho_arquivo
    return None

# Função para converter arquivos entre formatos suportados
def converter_arquivo(arquivo, formato):
    try:
        # Obtém a extensão do arquivo
        extensao = os.path.splitext(arquivo)[1].lower()

        # Converte imagens entre formatos suportados
        if extensao in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            imagem = Image.open(arquivo)
            nome = os.path.splitext(arquivo)[0]
            novo_arquivo = f"{nome}.{formato}"
            imagem.save(novo_arquivo, formato.upper())
            return f"Imagem convertida: {novo_arquivo}"

        # Converte arquivos Word para PDF
        elif extensao in [".doc", ".docx"] and formato == "pdf":
            logging.getLogger("comtypes").setLevel(logging.CRITICAL)
            import comtypes.client
            word = comtypes.client.CreateObject('Word.Application')
            doc = word.Documents.Open(arquivo)
            novo_arquivo = f"{os.path.splitext(arquivo)[0]}.pdf"
            doc.SaveAs(novo_arquivo, FileFormat=17)  # 17 é o formato para PDF
            doc.Close()
            word.Quit()
            return f"Arquivo Word convertido para PDF: {novo_arquivo}"

        # Converte arquivos PDF para Word
        elif extensao == ".pdf" and formato in ["docx", "doc"]:
            novo_arquivo = f"{os.path.splitext(arquivo)[0]}.docx"
            converter = pdf2docx.Converter(arquivo)
            converter.convert(novo_arquivo, start=0, end=None)
            converter.close()
            return f"Arquivo PDF convertido para Word: {novo_arquivo}"

        # Caso o formato ou extensão não sejam suportados
        else:
            return "Erro: Tipo de arquivo ou formato de conversão não suportado."

    except Exception as e:
        return f"Erro ao converter arquivo: {e}"


