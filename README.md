# Atividade Autônoma (AA) de Redes de Computadores (INF01154)

Criar um programa em TCP que permita analisar equidade do tráfego na rede.

O programa deve enviar dados na máxima velocidade possível pela rede (no laboratório é de 1G bit/s).
Um parâmetro de entrada deve ser a porta a ser utilizada, e as conexões podem ser feitas de forma par a par (cliente-servidor).
A rede deve ser monitorada por alguma ferramenta específica (No Linux o System Monitor, por exemplo. No Windows o Netmeter EVO, por exemplo).
O programa deve, obrigatoriamente, gerar um log com a média de tráfego por segundo (em bit/s).

* Parte 1: Apresentar gráfico com conexão entre duas máquinas (uma janela de terminal no servidor e uma no cliente).

* Parte 2: Expandir a conexão para mais um cliente (duas janelas de terminal no servidor e duas no cliente. Cada cliente x servidor numa porta diferente).

* Parte 3: Expandir a conexão para mais um cliente (três janelas de terminal no servidor e três no cliente. Cada cliente x servidor numa porta diferente).

O programa deve ser apresentado ao professor de forma individual em algum momento durante a disciplina até o deadline (intervalo de aulas ou a combinar). O algoritmo deve ser explicado verbalmente, mostrando o código-fonte e o resultado. A linguagem do programa é da escolha do aluno.

## Execução

A implementação das funcionalidades foram atribuídas a duas aplicações, `server` e `client`, que recebem e enviam dados, respectivamente.
O servidor é utilizado para salvar o log de velocidades. 

### Servidor
```./server.py --port <port> --output <filename.csv>```

Porta onde o processo deve esperar conexões e o arquivo onde os dados devem ser salvos, em formato CSV.
O endereço do host é informado durante a inicialização pelo programa.

### Cliente
```./server.py --port <port> --host <host>```

Porta e host do servidor para conexão.
Após a execução pelo tempo necessário, a conexão deve ser finalizada pelo cliente via CTRL+C, encerrando o programa, pois o servidor estará escrevendo no arquivo de log até o encerramento da conexão.

## Resultados
Após obter os dados pelo uso das aplicações de Servidor e Cliente, os dados podem ser analisados com o programa gerador de gráficos.

```./generate_graph.py <file1.csv> (file2.csv) (file3.csv) ... (fileN.csv)```

Irá abrir os arquivos CSV gerados por `server.py` e dispor em um gráfico de linhas, sendo cada linha representativa da conexão obtida e armazenada em cada arquivo CSV de entrada.


## Licença

Licença MIT. [Clique aqui para mais informações.](LICENSE.md)

 