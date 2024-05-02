# PBL-REDES-1

## Aplicação de Gerenciamento de Sensores (Client Side)
Esta aplicação permite aos usuários gerenciar sensores que pertencem a diferentes unidades de controle. Os usuários podem se conectar a uma unidade de controle, instanciar sensores, excluir sensores, desligar sensores e ligar sensores.

#### Instalar Python:
 Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em python.org.
##### Instalar Pacotes Necessários: 
 Esta aplicação utiliza os pacotes tkinter, requests e threading. Você pode instalá-los usando o pip:

    pip install tk requests

- Clonar o Repositório: Clone este repositório em sua máquina local.
- Executar a Aplicação: Abra um terminal ou prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/app) e execute o seguinte comando:
    python cliente .py

Uso: Ao executar a aplicação, uma janela será exibida solicitando que você insira um nome para ser seu identificador. Insira seu identificador e clique no botão "Confirmar". Uma vez confirmado, a janela principal da aplicação será exibida.
#### Funcionalidades
* Conectar a uma Unidade de Controle: Clique no botão "Conectar a uma UC" para se conectar a uma unidade de controle. Você será solicitado a inserir o nome da unidade de controle. Após a conexão, seu identificador será inscrito na unidade de controle.
* Instanciar Sensores: Clique no botão "Instanciar um ou mais sensores" para instanciar um ou mais sensores para uma unidade de controle específica. Por padrão, o nome da unidade de controle é definido como "TST" e o número de sensores é definido como 4. Você pode alterar esses valores no código, se necessário.
* Excluir Sensor: Esta funcionalidade ainda não está implementada.
* Desligar Sensor: Esta funcionalidade ainda não está implementada.
* Ligar Sensor: Esta funcionalidade ainda não está implementada.
Notas
A aplicação usa uma GUI simples construída com Tkinter.
Ela se comunica com um servidor em execução em localhost:8080. Certifique-se de que o servidor esteja em execução antes de usar a aplicação.

## Como Executar
