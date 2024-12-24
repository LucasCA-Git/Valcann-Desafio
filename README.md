![ValcannLogo](/public/Captura%20de%20tela%202024-12-24%20143050.png)

# **Valcann Programa de estágio** 

# **Automação de Backups** 

Este projeto é um script em Python para automatizar tarefas de gerenciamento de backups. Ele realiza as seguintes ações:

1. **Listar Arquivos**: Lista todos os arquivos em um diretório de origem, com detalhes como nome, tamanho, data de criação e data da última modificação. O resultado é salvo em um arquivo de log.  
2. **Excluir Arquivos Antigos**: Remove arquivos com mais de 3 dias da pasta de origem.  
3. **Copiar Arquivos Recentes**: Move arquivos com menos de 3 dias para um diretório de destino.  
4. **Gerar Logs**: Salva os detalhes dos arquivos em arquivos de log separados para as pastas de origem e destino.  
5. **Seleção de Diretórios**: Utiliza um popup para selecionar o diretório de origem.

## **Estrutura do Projeto**

* `script.py`: Arquivo principal com o código do script.  
* `logs/`: Diretório onde os arquivos de log serão salvos.  
  * `bckpExemplo.log`: Log dos arquivos processados.

## **Requisitos**

Para executar este script, é necessário ter o Python 3 instalado e as dependências abaixo:

### **Dependências**

* `tkinter`: Utilizado para abrir a interface de seleção de pastas.  
* `shutil`: Biblioteca padrão para manipulação de arquivos e diretórios.

### **OBS:** O tkinter é parte da biblioteca padrão do Python e geralmente vem pré-instalado, mas se caso não estiver coloquei um requirements.txt 

Instale as dependências com o comando abaixo:
```bash
pip install \-r requirements.txt
```
Conteúdo do arquivo `requirements.txt`:
```
tk
```
## **Como Usar**

1. **Configuração do Ambiente**:  
   * Certifique-se de que o diretório de destino (padrão: `temp`) existe ou permita que o script o crie automaticamente.  
2. **Execução do Script**:  
   * Execute o arquivo `script.py`:  
  ```bash
     python script.py  
  ```
3. **Interação**:  
   * Um popup será exibido para selecionar o diretório de origem no seu disco C.  
4. **Resultados**:  
   * Arquivos antigos serão excluídos do diretório de origem.  
   * Arquivos recentes serão copiados para o diretório de destino `D:/temp`.  
   * Logs serão salvos em:  
   * Origem:  `home/valcann/backupsFrom`  
   * Destino: `home/valcann/backupsTo`

## **Observações**

* Caso o diretório de origem ou destino não seja selecionado, o script será encerrado.  
* Certifique-se de ter permissões adequadas para acessar e manipular os arquivos nos diretórios selecionados.

## **Exemplo de Saída no Log**

Arquivo de log gerado:
```log
Nome: arquivo1.txt, Tamanho: 1024 bytes, Criado: 2024-12-20 10:30:45, Modificado: 2024-12-21 12:15:30  
Nome: arquivo2.txt, Tamanho: 2048 bytes, Criado: 2024-12-22 11:45:00, Modificado: 2024-12-23 14:00:00
```
## **Funções do Código**

#### **1\. Selecionar Pasta**

```python  

def selecionar_pasta(mensagem):  
    root = Tk()  
    root.withdraw()  # Oculta a janela principal  
    caminho_pasta = filedialog.askdirectory(title=mensagem)  
    return caminho_pasta
```
* Abre um popup para o usuário selecionar uma pasta.  
* Retorna o caminho da pasta escolhida.

#### **2\. Listar Arquivos com Detalhes**

```python  
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
```        

* Lista os arquivos em um diretório e salva os detalhes (nome, tamanho, data de criação e modificação) em um arquivo de log.  
* Usa `os.stat` para obter informações dos arquivos.

#### **3\. Processar Arquivos**

```python  

def processar_arquivos(pasta_origem, pasta_destino):  
    try:  
        agora = datetime.now()  
        data_limite = agora - timedelta(days=3)

        for nome_arquivo in os.listdir(pasta_origem):  
            caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)  
            if os.path.isfile(caminho_arquivo):  
                data_criacao = datetime.fromtimestamp(os.stat(caminho_arquivo).st_ctime)  
                if data_criacao > data_limite:  
                    os.remove(caminho_arquivo) 
                    print(f"Arquivo deletado: {nome_arquivo}")  
                else:  
                    caminho_destino = os.path.join(pasta_destino, nome_arquivo)  
                    shutil.copy2(caminho_arquivo, caminho_destino)  
                    print(f"Arquivo copiado: {nome_arquivo} para {pasta_destino}")  
    except Exception as e:  
        print(f"Erro ao processar arquivos: {e}")
```
* Define a data limite como 3 dias atrás.  
* Remove arquivos criados há mais de 3 dias.  
* Copia arquivos recentes para o diretório de destino.

---

### **Bloco Principal**

```python  
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
```

1. Solicita ao usuário a seleção das pastas de origem e destino usando a função `selecionar_pasta`.  
2. Verifica se ambas as pastas foram selecionadas, caso contrário, encerra o programa.  
3. Salva os logs da pasta de origem em `backupsFrom.log`.  
4. Processa os arquivos: remove antigos e copia recentes.  
5. Salva os logs da pasta de destino em `backupsTo.log`.  
6. Exibe mensagens indicando o progresso das operações.



## **Licença**

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

