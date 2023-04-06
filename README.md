# dgenerate

A simple utility to stand up a kafka cluster in docker, then start a continuous flow of fake data for testing and development purposes.

## Setup 
To run do:
```
git clone git@github.com:kgorman/dgenerate.git
cd dgenerate
docker-compose up
```

This will populate the topic 'traffic' with fake internet traffic. The topic retention policy can be altered in the docker compose file, it's set to 1 hour by default.

## using kcat

If you would like to inspect the data via kcat, one way is to add an /etc/hosts entry:
- Alter /etc/hosts to add `127.0.0.1 kafka`
- Run kcat as normal against using `localhost:9092` as the broker.
