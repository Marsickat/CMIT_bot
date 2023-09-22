run:
	poetry run python -m bot

generate:
	poetry run alembic revision --m="$(NAME)" --autogenerate

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1
