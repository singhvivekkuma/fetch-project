# fetch-project

## Overview
This project implemets a Kafka Consumer to support streaming of data using Python and Docker

## Setup Instructions
### 1. Install **Docker** and **Docker Compose**
#### a. Use [Docker Desktop](https://docs.docker.com/desktop/) to get the latest version of Docker (Docker Desktop) and follow the Docker instalation guide
#### b. Verify Installation: Run the following command in your terminal:
```
    docker --version
    docker-compose --version
```


### 2. Clone this repository:
```
    git clone https://github.com/singhvivekkuma/fetch-project
    cd fetch-project
```

### 3. Start Kafka Services
```
    docker-compose up -d
```
#### This should show running Kafka, Zookeeper, and Data Generator
```
    docker ps
```

### 4. Run the consumer
```
    python consumer.py
```

####       If you've confirmed that messages are being processed and published correctly, you can stop the consumer using ```Ctrl + C```.
####        If you restart the consumer later, it will resume reading messages based on the Kafka offset settings.

### 5. Verify the processed messages
####        a. Open Kafka Container Cell:
```
    docker exec -it $(docker ps --filter "ancestor=confluentinc/cp-kafka" -q) bash
```

####        b. Consume Messages from the new topic:
##### Inside the kafka container run below commaned, this will display all the processed messages that were published.
```
    kafka-console-consumer --bootstrap-server localhost:9092 --topic processed-user-login --from-beginning
```

##### Once you have confirmed that the processed messages are as expected, use ```Ctrl + C``` and  ```exit```. You should be back to *\fetch_project path.


## Technology Used
1. Docker & Docker Compose
2. Kafka
3. Python
4. Confluent Kafka Library