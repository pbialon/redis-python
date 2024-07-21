test:
	pipenv run python -m unittest discover
	
install:
	pipenv install --dev

run:
	pipenv run python -m app.main ${PARAMS}