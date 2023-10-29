# Instruções para Configuração do Projeto

Siga os passos abaixo para configurar e executar este projeto:

## Requisitos

Certifique-se de ter o Python 3.10 instalado em sua máquina. Você pode verificar a versão atual do Python com:
```shell
python --version
```
ou 
```shell
python3 --version
```
Para garantir que você está utilizando a versão 3.10.

## 1. Criação do Ambiente Virtual

Comece criando um ambiente virtual no diretório onde se encontram os arquivos do projeto. Se você já tiver o Python 3.10 instalado, pode criar o ambiente virtual usando:

**No Linux/macOS:**
```shell
python3.10 -m venv venv
```

**No Windows:**
```shell
py -3.10 -m venv venv
```

## 2. Ativação do Ambiente Virtual

Após a criação, é necessário ativar o ambiente virtual. 

**No Linux/macOS:**
```shell
source venv/bin/activate
```

**No Windows:**
```shell
venv\Scripts\activate
```

## 3. Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências do projeto através do comando:
```shell
pip install -r requirements.txt
```

## 4. Execução do Projeto

Agora, abra o terminal e execute o seguinte comando para iniciar a aplicação:
```shell
streamlit run graph.py
```

Após executar este comando, será aberta uma guia no navegador com os gráficos em uma interface web.

---

Aproveite o projeto! 😊
