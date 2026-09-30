# Cantina do Pablo

Sistema desktop de pedidos e gerenciamento da Cantina do Pablo, desenvolvido em Python, PySide6 e ReportLab.

## Requisitos

- Python 3.10 ou superior
- Windows, Linux ou macOS
- `pip`

## Instalação com ambiente virtual

Abra o terminal na pasta do projeto.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python cantina.py
```

Se o PowerShell bloquear a ativação do ambiente virtual, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python cantina.py
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python cantina.py
```

## Execução

Com o ambiente virtual ativado:

```bash
python cantina.py
```

O programa abre o totem da Cantina do Pablo e solicita a senha para acesso ao painel administrativo.

## Administração de produtos

No painel administrativo existe o botão **Produtos**.

É possível:

- cadastrar produtos;
- editar produtos existentes;
- excluir produtos;
- alterar nome;
- alterar descrição;
- alterar preço;
- escolher a categoria;
- selecionar uma imagem do computador;
- visualizar a imagem antes de salvar.

As alterações ficam salvas em `produtos.json` e passam a ser usadas pelo totem.

As imagens selecionadas são copiadas para a pasta `imagens`.

## Comandas

Os pedidos confirmados são registrados em `comandas_pendentes.json`.

Cada pedido gera um PDF dentro da pasta `comandas`, com:

- nome do cliente;
- número da comanda;
- data e horário;
- produtos;
- quantidades;
- preços unitários;
- subtotais;
- valor total;
- identificação da Cantina do Pablo.

## Dependências

As dependências estão no arquivo `requirements.txt`.

Para instalar:

```bash
python -m pip install -r requirements.txt
```

## Estrutura principal

```text
Cantina/
├── cantina.py
├── requirements.txt
├── README.md
├── produtos.json
├── comandas_pendentes.json
├── contador_comandas.json
├── assets/
├── imagens/
└── comandas/
```

## Tema visual

A interface usa tema escuro com verde como cor de destaque, sem emojis.
As cores ficam no início do `cantina.py`, nas constantes `COR_*`, e os estilos
compartilhados (botões, campos, listas, barras de rolagem e caixas de diálogo)
ficam em `ESTILO_GLOBAL` e nas funções `estilo_btn_*`. Para trocar a paleta,
basta alterar essas constantes.
