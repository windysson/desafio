setup:
	pip install -r requirements.txt
part1:
	docker-compose up -d
	cd part1/
	alembic init migrations
	#arquivo alembic.ini troca a sqlalchemy.url = mysql+pymysql://root:password@localhost:3307/aeroporto e coloque o arquivo create_passengers_table.py em migrations/versions/
	alembic upgrade head
	python donwload.py
	python popular_banco.py
part2:
	cd part2
	python preparacao_banco.py
	python treinamento.py
	python atualizacao.py
part3:
	cd part3
	python graficos.py
