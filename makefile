.PHONY: db-migrate
db-migrate:
	alembic revision --autogenerate

.PHONY: db-upgrade
db-upgrade:
	alembic upgrade head

.PHONY: db-downbase
db-downbase: 
	alembic downgrade base

.PHONY: run
run:
	flask --app app run --debug