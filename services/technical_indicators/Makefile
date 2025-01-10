run-dev:
# @echo is used to print the message to the console
	@echo "Loading environment variables from .env..."
# @export is used to set the environment variables in the current shell
	@export VIRTUAL_ENV=$(PWD)/.venv && uv run python run.py

build:
	docker build -f Dockerfile -t technical_indicators .

run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		technical_indicators