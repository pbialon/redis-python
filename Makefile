test:
	pipenv run python -m unittest discover
	
install:
	pipenv install --dev

format:
	pipenv run black .

lint: format
fmt: format