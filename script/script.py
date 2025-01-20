import os
import shutil
from datetime import datetime, timedelta
from tkinter import Tk, filedialog

# Função para abrir um popup de seleção de pasta
def selecionar_pasta(mensagem):
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    caminho_pasta = filedialog.askdirectory(title=mensagem)
    return caminho_pasta

# Função para listar arquivos com detalhes e salvar em um log
def listar_arquivos_com_detalhes(caminho_pasta, arquivo_log):
    try:
        with open(arquivo_log, 'w') as log:
            for nome_arquivo in os.listdir(caminho_pasta):
                caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                if os.path.isfile(caminho_arquivo):
                    estatisticas = os.stat(caminho_arquivo)
                    tamanho = estatisticas.st_size
                    data_criacao = datetime.fromtimestamp(estatisticas.st_ctime)
                    data_modificacao = datetime.fromtimestamp(estatisticas.st_mtime)
                    log.write(f"Nome: {nome_arquivo}, Tamanho: {tamanho} bytes, Criado: {data_criacao}, Modificado: {data_modificacao}\n")
        print(f"Detalhes dos arquivos salvos em {arquivo_log}")
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

# Função para processar arquivos
def processar_arquivos(pasta_origem, pasta_destino):
    try:
        agora = datetime.now()
        data_limite = agora - timedelta(days=3)

        for nome_arquivo in os.listdir(pasta_origem):
            caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)
            if os.path.isfile(caminho_arquivo):
                data_criacao = datetime.fromtimestamp(os.stat(caminho_arquivo).st_ctime)
                if data_criacao < data_limite:  # Arquivos mais antigos que 3 dias
                    os.remove(caminho_arquivo)
                    print(f"Arquivo deletado: {nome_arquivo}")
                else:  # Arquivos mais novos ou com exatamente 3 dias
                    caminho_destino = os.path.join(pasta_destino, nome_arquivo)
                    shutil.copy2(caminho_arquivo, caminho_destino)
                    print(f"Arquivo copiado: {nome_arquivo} para {pasta_destino}")
    except Exception as e:
        print(f"Erro ao processar arquivos: {e}")

if __name__ == "__main__":
    print("Selecione a pasta de origem para os backups...")
    pasta_origem = selecionar_pasta("Selecione a pasta de origem (/home/valcann/backupsFrom)")

    print("Selecione a pasta de destino para os backups...")
    pasta_destino = selecionar_pasta("Selecione a pasta de destino (/home/valcann/backupsTo)")

    if not pasta_origem or not pasta_destino:
        print("Pasta de origem ou destino não selecionada. Saindo...")
        exit()

    log_origem = os.path.join(pasta_origem, "backupsFrom.log")
    log_destino = os.path.join(pasta_destino, "backupsTo.log")

    print("Listando arquivos na pasta de origem...")
    listar_arquivos_com_detalhes(pasta_origem, log_origem)

    print("Processando arquivos...")
    processar_arquivos(pasta_origem, pasta_destino)

    print("Listando arquivos na pasta de destino...")
    listar_arquivos_com_detalhes(pasta_destino, log_destino)

    print("Automação de backups concluída com sucesso!")
