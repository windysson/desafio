# Data Manupulation

## Recursos

1. <https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018>
2. <https://pypi.org/project/kaggle/>
3. <https://www.docker.com/>

## Descrição

Nesta etapa você irá construir sua base de dados usando o dataset do item 1. É recomendado utilizar o pacote do kaggle para python para realizar o download. Você precisa ingerir os dados em algum banco de dados (relacional ou não) no tempo mais rápido que conseguir.

Os dados precisam ser os mesmos que estão nos arquivos CSVs do dataset passado, porém toda linha precisa adicionar o campo createdAt que identifica quando o dado foi inserido. Este novo campo precisa obrigatóriamente ser do tipo datetime e conter os o ano, mês, dia, hora, minuto, segundo, milesimo de segundo.

Os dados faltantes nas linhas precisam ser inseridos padronizados. Ou seja, onde está null e for um campo numérico, deve-se inserir umn dado padrão que não afetará o resultado.

## Definição de concluído

1. Arquivo de docker com o banco de dados definido (ou recurso externo).
2. Se optar por SQL, deve-se ter o esquema do banco de dados criado por migrations. Caso opte por usar ORM, deve-se escrever um paragráfo no PR explicando a necessidade do seu uso.
3. Os dados precisam está neste banco de dados com os dados formatados como descrito.
