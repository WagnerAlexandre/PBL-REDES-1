# PBL-REDES-1

## Aplicação de Gerenciamento de Sensores (Client Side)
Esta aplicação permite aos usuários gerenciar sensores que pertencem a diferentes unidades de controle. Os usuários podem se conectar a uma unidade de controle, instanciar sensores, excluir sensores, desligar sensores e ligar sensores.

#### Instalar Python:
 Certifique-se de ter o Python instalado em seu sistema. Você pode baixá-lo em python.org.
##### Instalar Pacotes Necessários: 
 Esta aplicação utiliza os pacotes tkinter, requests e threading. Você pode instalá-los usando o pip:
> pip install tk requests

- Clonar o Repositório: Clone este repositório em sua máquina local.
- Executar a Aplicação: Abra um terminal ou prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/app) e execute o seguinte comando:
    > python cliente.py

Uso: Ao executar a aplicação, uma janela será exibida solicitando que você insira um nome para ser seu identificador. Insira seu identificador e clique no botão "Confirmar". Uma vez confirmado, a janela principal da aplicação será exibida.
#### Funcionalidades
* Conectar a uma Unidade de Controle: Clique no botão "Conectar a uma UC" para se conectar a uma unidade de controle. Você será solicitado a inserir o nome da unidade de controle. Após a conexão, seu identificador será inscrito na unidade de controle.
* Instanciar Sensores: Clique no botão "Instanciar um ou mais sensores" para instanciar um ou mais sensores para uma unidade de controle específica. Uma nova janela será aberta para que seja digitado o nome da unidade de controle, ao confirmar o nome da unidade de controle, uma outra janela aparecerá para que seja digitado o número de sensores.
* Excluir Sensor: Exclui o sensor selecionado na tabela.
* Desligar Sensor: Desliga o sensor selecionado na tabela.
* Ligar Sensor: Liga o sensor selecionado na tabela.

##### Notas
 A aplicação usa uma GUI simples construída com Tkinter.
 Ela se comunica com um servidor em execução em localhost:8080. Certifique-se de que o servidor esteja em execução antes de usar a aplicação.

## Servidor da API de Gerenciamento de Sensores
 Esta é a API de gerenciamento de sensores, que implementa os endpoints para manipular unidades de controle e sensores.

### Execução do Servidor
* Instalar Go: Certifique-se de ter Go instalado em seu sistema. Você pode baixá-lo em golang.org.
* Clonar o Repositório: Clone este repositório em sua máquina local.
* Executar o servidor: Abra um terminal ou       prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/server/api)e execute o seguinte comando:
    > go run main.go

#### Uso da API
 Após iniciar o servidor, você pode fazer requisições HTTP para os endpoints.


## Controladora de Sensores
 A controladora de sensores é responsável por gerenciar os sensores conectados e executar comandos enviados por outros dispositivos.

### Funcionalidades
* Instanciar um Novo Sensor: Adiciona um novo sensor à lista de sensores disponíveis.
Excluir um Sensor: Remove um sensor da lista de sensores.
* Ligar um Sensor: Inicia a transmissão de dados de um sensor para a unidade de controle.
Desligar um Sensor: Para a transmissão de dados de um sensor.
* Visualizar os Sensores: Exibe uma lista dos sensores disponíveis e sua última leitura.

#### Descrição dos Comandos
1. Instanciar um Novo Sensor
 Comando: 1
 Descrição: Adiciona um novo sensor à lista de sensores disponíveis.
 Entrada: Não requer entrada adicional.
 Saída: Exibe o ID do novo sensor instanciado.
2. Excluir um Sensor
 Comando: 2
 Descrição: Remove um sensor da lista de sensores.
 Entrada: ID do sensor a ser excluído.
 Saída: Confirmação da exclusão do sensor.
3. Ligar um Sensor
 Comando: 3
 Descrição: Inicia a transmissão de dados de um sensor para a unidade de controle.
 Entrada: ID do sensor a ser ligado.
 Saída: Confirmação de que o sensor foi ligado.
4. Desligar um Sensor
 Comando: 4
 Descrição: Para a transmissão de dados de um  sensor.
 Entrada: ID do sensor a ser desligado.
 Saída: Confirmação de que o sensor foi desligado.
5. Visualizar os Sensores
 Comando: 5
 Descrição: Exibe uma lista dos sensores disponíveis e sua última leitura.
 Entrada: Não requer entrada adicional.
 Saída: Lista dos sensores disponíveis e suas últimas leituras.
#### Execução da Controladora

- Executar a Controladora: Abra um terminal ou prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/device) e execute o seguinte comando:
    > python controller.py
- Interagir com a Controladora: Utilize os comandos numéricos listados acima para interagir com a controladora e gerenciar os sensores.