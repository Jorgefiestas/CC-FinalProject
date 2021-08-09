.PHONY: app

app:
	cd app/docker; docker build -t webapp:beta .
all:
	kubectl apply -R -f .
