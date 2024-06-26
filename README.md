# PBL 1 - Concorrência e conectividade - Aplicação de gerenciamento de dispositivos via Servidor
-----
### Sumario

  * [Introdução](#introdução)
  * [Como utilizar a aplicação](#como-utilizar-a-aplicação)
  * * [Aplicação de Gerenciamento de Sensores (Client Side)](#aplicação-de-gerenciamento-de-sensores-client-side)
  * * [Servidor/Broker para o Gerenciamento de Sensores](#servidorbroker-para-o-gerenciamento-de-sensores)
  * * [Controladora de Sensores](#controladora-de-sensores)
  * [Sobre o Sistema](#sobre-o-sistema)
  * * [Arquitetura da solução](#arquitetura-da-solução)
  * * [Protocolo de comunicação entre dispositivo e Broker - camada de aplicação](#protocolo-de-comunicação-entre-dispositivo-e-broker---camada-de-aplicação)
  * * [Protocolo de comunicação entre dispositivo e Broker - camada de transporte:](#protocolo-de-comunicação-entre-dispositivo-e-broker---camada-de-transporte)
  * * [Interface da Aplicação (REST):](#interface-da-aplicação-rest)
  * * [Formatação, envio e tratamento de dados](#formatação-envio-e-tratamento-de-dados)

  * * [Tratamento de conexões simultâneas](#tratamento-de-conexões-simultâneas)
  * * [Desempenho](#desempenho)
----
## Introdução

 Como método de avaliação da disciplina de MI - Concorrência e Conectividade [TEC502] do curso de Engenharia de Computação da Universidade Estadual Feira de Santana (UEFS) do semestre 2024.1, foi proposto o desenvolvimento de sistema de gerenciamento de dispositivos (sensor/atuador) via uma aplicação conectada a um servidor.
 O sistema a ser desenvolvido deve:

1. Possuir um dispositivo virtual para geração de dados fictícios que:
    1. Utiliza um sistema não confiável de envio de dados para o servidor.
    2. Tenha uma interface por parâmetros para manipulação direta dos dados e do próprio dispositivo.
2. Possuir uma interface de interação com o usuário que:
    1. Permita a manipulado dos dispositivos conectados pelo usuário.
    2. Visualização das informações geradas pelos dispositivos.
3. O sistema deve comunicar a interface do usuário com os dispositivos por meio de uma API REST.




----
## Como utilizar a aplicação
### Aplicação de Gerenciamento de Sensores (Client Side)
 Esta aplicação permite aos usuários gerenciar sensores que pertencem a diferentes unidades de controle. Os usuários podem se conectar a uma unidade de controle, instanciar sensores, excluir sensores, desligar sensores e ligar sensores.

##### Instalar Python:
 Certifique-se de ter o *Python 3.11* instalado em seu sistema. Você pode baixá-lo em python.org.

##### Instalar Pacotes Necessários: 
 Esta aplicação utiliza os pacotes *tkinter*, requests e threading. Você pode instalá-los usando o pip:
> pip install tk requests

- Clonar o Repositório: Clone este repositório em sua máquina local.
- Executar a Aplicação: Abra um terminal ou prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/app) e execute o seguinte comando:
    > python cliente.py

 Uso: Ao executar a aplicação, uma janela será aberta, nesta janela, além de uma tabela que irá dispor os sensores conectados há algumas opções.
#### Funcionalidades
* Conectar a uma Unidade de Controle: Clique no botão "Conectar a uma UC" para se conectar a uma unidade de controle. Você será solicitado a inserir o nome da unidade de controle. Após a conexão, a aplicação começara a requisitar os sensores instanciados naquela unidade de controle.
* Instanciar Sensores: Clique no botão "Instanciar um ou mais sensores" para instanciar um ou mais sensores para uma unidade de controle específica. Uma nova janela será aberta para que seja digitado o nome da unidade de controle, ao confirmar o nome da unidade de controle, uma outra janela aparecerá para que seja digitado o número de sensores.
* Excluir Sensor: Exclui o sensor selecionado na tabela.
* Desligar Sensor: Desliga o sensor selecionado na tabela.
* Ligar Sensor: Liga o sensor selecionado na tabela.

##### Notas
 A aplicação usa uma GUI simples construída com Tkinter.

 
-----------------
### Servidor/Broker para o Gerenciamento de Sensores
 Este é o servidor/broker de gerenciamento de sensores, que implementa os endpoints para manipular unidades de controle e sensores.

#### Execução do Servidor
* Instalar Go: Certifique-se de ter *Go* instalado em seu sistema. Você pode baixá-lo em golang.org.
* Clonar o Repositório: Clone este repositório em sua máquina local.
* Executar o servidor: Abra um terminal ou prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/server) e execute o seguinte comando:
    > go run main.go

#### Uso da API
 Após iniciar o servidor, você pode fazer requisições HTTP para os endpoints.

-----------------
### Controladora de Sensores
 A controladora de sensores é responsável por gerenciar os sensores conectados e executar comandos enviados por outros dispositivos.
 Cada unidade controladora é capaz de instanciar vários sensores.

#### Funcionalidades
* Instanciar um Novo Sensor: Adiciona um novo sensor à lista de sensores disponíveis.
Excluir um Sensor: Remove um sensor da lista de sensores.
* Ligar um Sensor: Inicia a transmissão de dados de um sensor para a unidade de controle.
Desligar um Sensor: Para a transmissão de dados de um sensor.
* Visualizar os Sensores: Exibe uma lista dos sensores disponíveis e sua última leitura.

#### Descrição dos Comandos
+ Instanciar um Novo Sensor
  + Comando: 1
    Descrição: Adiciona um novo sensor à lista de sensores disponíveis.
    Entrada: Não requer entrada adicional.
    Saída: Exibe o ID do novo sensor instanciado.
+ Excluir um Sensor.
  + Comando: 2
    Descrição: Remove um sensor da lista de sensores.
    Entrada: ID do sensor a ser excluído.
    Saída: Confirmação da exclusão do sensor.
+ Ligar um Sensor.
  + Comando: 3
    Descrição: Inicia a transmissão de dados de um sensor para a unidade de controle.
    Entrada: ID do sensor a ser ligado.
    Saída: Confirmação de que o sensor foi ligado.
+ Desligar um Sensor.
  + Comando: 4
    Descrição: Para a transmissão de dados de um  sensor.
    Entrada: ID do sensor a ser desligado.
    Saída: Confirmação de que o sensor foi desligado.
+ Visualizar os Sensores.
  + Comando: 5
    Descrição: Exibe uma lista dos sensores disponíveis e sua última leitura.
    Entrada: Não requer entrada adicional.
    Saída: Lista dos sensores disponíveis e suas últimas leituras.

#### Execução da Controladora

- Executar a Controladora: Abra um terminal ou prompt de comando, navegue até o diretório que contém o código (PBL-REDES-1/device) e execute o seguinte comando:
    > python controller.py
- Interagir com a Controladora: Utilize os comandos numéricos listados acima para interagir com a controladora e gerenciar os sensores.

---- 
## Sobre o Sistema
#### Arquitetura da solução
O sistema desenvolvido como solução foi dividido em três partes:
1. Aplicação de gerenciamento:
    1.  Esta parte da solução é a interface do usuário para o sistema.
    2.  Desenvolvida usando Tkinter, uma biblioteca gráfica para Python.
    3.  Permite ao usuário visualizar os dados dos sensores e interagir com o sistema de gerenciamento de forma intuitiva.
    4.  Realiza operações como conectar-se a UCs, instanciar, excluir, ligar e desligar sensores através de solicitações HTTP para a API do servidor/broker.

2. Servidor/Broker - O servidor possui o serviço *Broker* e API REST integradas.
    1.  O servidor possui o serviço de Broker e uma API REST integrada.
    2.  Responsável por receber e processar as solicitações da aplicação de gerenciamento.
    3.  Implementa lógica para conectar UCs, instanciar, excluir, ligar e desligar sensores ao enviar dados via TCP/IP para respectivas UC's e sensores.
    4.  Gerencia a comunicação entre a aplicação de gerenciamento e as UCs, se necessário.

3. Unidade de Controle - Como forma de melhor gerenciar diversos dispositivos, foi escolhido instanciar conjuntos de dispositivos em um conjunto, este chamado de Unidade de Controle.
    1.  Os dispositivos virtuais escolhidos para gerar os dados foram sensores de temperatura. 
    2.  Responsável por gerenciar os sensores instanciados e processar as solicitações da aplicação de gerenciamento.


#### Comunicação entre Componentes:
##### Aplicação de Gerenciamento <-> Servidor/Broker:
A aplicação de gerenciamento se comunica com o servidor/broker através de solicitações HTTP para a API REST para enviar solicitações para conectar-se a UCs, instanciar, excluir, ligar e desligar sensores e ainda recebe respostas do servidor/broker para confirmar o sucesso ou falha das operações.

##### Servidor/Broker <-> Unidade de Controle (UC):
O servidor/broker se comunica com as UCs para receber dados dos sensores e enviar comandos para ligar ou desligar sensores, se utilizando da combinação de sockets TCP/IP, o servidor foi projeto para lidar de maneira assíncrona a cada acesso, inciando go routines para cada conexão.


#### Protocolo de comunicação entre dispositivo e Broker - camada de aplicação
Na troca de mensagens entre as UCs (Unidades de Controle) e o broker, foram definidos os seguintes protocolos:

* Protocolo de Registro da UC:
Quando uma UC é inicializada, ela se conecta ao servidor broker via TCP e envia uma mensagem de registro contendo seu nome (UCName) para se identificar no sistema.
    > O servidor broker verifica se já existe uma UC com o mesmo nome registrado. Se não existir, a UC é registrada com sucesso. Caso contrário, é enviado um código de erro para a UC informando que o nome já está em uso.
Esse protocolo utiliza uma mensagem com o tipo 1 para indicar o registro e é realizado sobre TCP.

* Protocolo de Controle de Sensores:
As UCs podem enviar comandos para o servidor broker para controlar os sensores. Esses comandos incluem instanciar um novo sensor, excluir um sensor existente, ligar um sensor específico e desligar um sensor específico.
    >Cada comando é enviado como uma mensagem de controle sobre TCP, contendo o tipo de comando (instanciar, excluir, ligar ou desligar) e os parâmetros necessários, como o ID do sensor.

* Protocolo de Atualização de Sensores:
Os dados dos sensores são enviados do dispositivo para o servidor broker via UDP em intervalos regulares. Cada mensagem UDP contém informações sobre o sensor, incluindo seu ID, temperatura e estado atual.
    Essas mensagens são transmitidas periodicamente para fornecer atualizações em tempo real sobre o estado dos sensores para o servidor broker.

#### Protocolo de comunicação entre dispositivo e Broker - camada de transporte:

Na camada de transporte, é utilizada tanto o protocolo TCP quanto UDP:
* TCP (Transmission Control Protocol):
    Na troca de mensagens de controle entre os dispositivos (UCs) e o servidor broker, como o registro da UC e os comandos de controle de sensores, o TCP é empregado. Isso garante que as mensagens sejam entregues de forma confiável e na ordem correta.
    Por exemplo, quando uma UC é inicializada, ela se conecta ao servidor broker via TCP e envia uma mensagem de registro contendo seu nome. O servidor broker verifica essa mensagem e envia uma resposta indicando se o registro foi bem-sucedido ou não.


* UDP (User Datagram Protocol):
        Na transmissão dos dados dos sensores do dispositivo para o servidor broker, o UDP é utilizado. Como os dados dos sensores são enviados em intervalos regulares e podem ser perdidos ocasionalmente sem afetar significativamente o sistema, o UDP é uma escolha adequada para essa finalidade.
        Cada mensagem UDP contém informações sobre o sensor, como seu ID, temperatura e estado atual. Essas mensagens são transmitidas periodicamente pelas UCs para fornecer atualizações em tempo real sobre o estado dos sensores para o servidor broker.


#### Interface da Aplicação (REST):
Na interface da aplicação, os verbos HTTP padrão (GET, POST, DELETE) são utilizados para interagir com os sensores. As rotas da API REST incluem:

>`/verificar`: Conectar-se a uma unidade de controle. (POST)
`/instSensor`: Instanciar um ou mais sensores.(POST)
`/excludeSensor`: Excluir um sensor.(POST)
`/ligarSensor`: Ligar um sensor.(POST)
`/desligarSensor`: Desligar um sensor.(POST)
`/sensors`: Obter dados dos sensores.(POST)

Para manter a API state-less, uma vez que não há propriamente um banco de dados rodando no servidor, foi necessário escrever as informações necessárias para cada acesso na requisição, por isso somente métodos POST foram utilizados.

#### Formatação, envio e tratamento de dados:

Os dados são formatados de acordo com o padrão JSON (JavaScript Object Notation). Isso possibilita que dispositivos e servidor compreendam as mensagens trocadas, garantindo a interoperabilidade entre diferentes nós do sistema. Após a transmissão, os dados são decodificados e processados pelo servidor para atualização do estado dos sensores ou execução das outras operações conforme necessário.

#### Tratamento de conexões simultâneas
Ao empregar go routines para lidar com cada tipo de acesso no servidor, não foi necessário lidar com acessos simultâneos, devido ao próprio GO já gerenciar automaticamente suas rotinas.

#### Desempenho
Visando minimizar o tempo de resposta da requisição das leituras, o sistema já guarda em uma especie de cache a ultima leitura feita por cada sensor conectado ao sistema.
Ainda, O uso de go routines separadas para cada tipo de acesso ao servidor, faz com que o mesmo lide com cada um de forma assíncrona, permitindo que cada solicitação seja processada "simultaneamente", aumentando a eficiência e throughput.
