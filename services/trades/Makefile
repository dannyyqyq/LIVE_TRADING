run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t trades .

run: build
# it allow to see logs within docker images from "image" (trade)
# - e overwrite config file with new value
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades

build-multistage:
	docker build -f multistage.Dockerfile -t trades:multistage .

run-multistage: build-multistage
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		trades:multistage

build-all: build build-multistage # builds both images 