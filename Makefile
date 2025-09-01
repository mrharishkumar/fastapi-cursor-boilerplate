.PHONY: lint format check fix clean run dev

lint:
	ruff check .

format:
	ruff format .

check:
	ruff check .
	ruff format --check .

fix:
	ruff check --fix .
	ruff format .

clean:
	ruff clean

run:
	python run.py

dev:
	uv run app:main --reload
