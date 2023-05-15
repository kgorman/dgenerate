# dgenerate

A simple utility to stand up a kafka cluster in docker, then start a continuous flow of fake data for testing and development purposes.

## Setup 
To run do:
```bash
git clone git@github.com:kgorman/dgenerate.git
cd dgenerate
docker-compose up
```

This will populate the topic 'traffic' with fake internet traffic. The topic retention policy can be altered in the docker compose file, it's set to 1 hour by default.

## Using kcat

If you would like to inspect the data via kcat, one way is to add an /etc/hosts entry:
- Alter /etc/hosts to add `127.0.0.1 kafka`
- Run kcat as normal using localhost as the broker `kcat -L -b localhost:9092` or `kcat -C -t traffic -b localhost:9092`

## New generators
This is simply a pattern of using faker to create data in kafka. If you want to add new data patterns alter generate.py to use any of the [faker libraries](https://faker.readthedocs.io/en/master/providers.html) available. As you test be sure to use something like this when restarting docker to ensure you are seeing your latest changes.
```bash
docker-compose down; docker-compose build --no-cache; docker-compose up
``` 