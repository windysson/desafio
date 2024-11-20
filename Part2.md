# Data Transformation

## Recursos

1. Banco de dados criado na etapa anterior
2. <https://scikit-learn.org/>

## Descrição

Nesta etapa espera-se que o banco de dados esteja populado. Agora chegou a hora de criar os insights para os usuários. Para isso você precisa criar uma nova coleção (ou tabela, ou o que desejar) que irá contem informações importantes para os usuários.

Nesta nova coleção é necessário gravar uma tupla por linha aerea, número do voo contendo e origem, contendo os dados:

- Média de tempo de delay (somatório dos campos CARRIER_DELAY, WEATHER_DELAY, NAS_DELAY, SECURITY_DELAY, LATE_AIRCRAFT_DELAY)
- Somatório do tempo que a aeronave permaneceu no voando (AIR_TIME)
- Chance do voo ser cancelado
  - Utilize o pacote scikit-learn para produzir esse valor
  - Crie um modelo simples que estime se o voo será cancelado ou não
  - Descreva no PR como chegou nessa solução e como pensou em resolver essa informação

## Definição de concluído

1. Banco de dados com nova coleção
2. Nova coleção populada com os dados corretos seguindo a descrição acima
3. Paragrafo contendo a informação de como solucionou o problema da chance de um voo ser cancelado
