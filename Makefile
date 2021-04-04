GIT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_NAME := "sfshare"

all: build

build:
	docker build -t wooh/$(IMAGE_NAME):$(GIT_SHA) --build-arg GIT_SHA_ARG=$(GIT_SHA) .


run:
	docker run -d -p 8080:80 wooh/$(IMAGE_NAME):$(GIT_SHA)
	sleep 3
	xdg-open http://localhost:8080

stop:
	docker stop $(docker ps | grep 'wooh/$(IMAGE_NAME)' | cut -d ' ' -f 1)


publish:
	docker push wooh/$(IMAGE_NAME):$(GIT_SHA)
