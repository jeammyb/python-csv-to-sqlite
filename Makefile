.PHONY: build run clean
default: build

IMAGE_FULL_NAME = boardgames-app:latest

build:
	docker build -t ${IMAGE_FULL_NAME} .


run:
	docker container run --rm -e FILE=${f} --name boardgames \
-v ${PWD}:/app/boardgames/ ${IMAGE_FULL_NAME}


clean:
	docker stop boardgames || true
	docker rm boardgames || true
	docker rmi boardgames-app:latest
