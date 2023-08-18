from prometheus_client import start_http_server, Gauge, CollectorRegistry
#from kafka import KafkaProducer
import random
import time
import json

topic='Prometheus'
#producer = KafkaProducer(bootstrap_servers='kafka:9092')
metric = Gauge('my_random_values', 'Random values with some anomalies')

def randomWithAnomaly(anomaly_threshold, anomaly_factor):
    number = random.random()
    #print("Initial number: ", number)
    if number < anomaly_threshold:
        number = number + anomaly_factor
        #print("Since the initial number is smaller than ", anomaly_threshold, ", the new number is ", number)
        return number
    else:
        #print("Since the initial number is greater than ", anomaly_threshold, ", the number remains unchanged: ", number)
        return number

if __name__ == '__main__':
    registry = CollectorRegistry()
    registry.register(metric)
    start_http_server(8000, registry=registry)
    while True:
        number = randomWithAnomaly(0.01, 3)
        metric.set(number)
        if number > 1:
            print(number, "WARNING: ANOMALY")
        else:
            print(number)
        '''
        data = {"fields": {
            "value": number
        },
        "name": "epic2",
        "tags": {
            "host": "Jaime"
        },
        "timestamp": time.time()
        }
        
        js = json.dumps(data).encode('utf8')
        producer.send(topic,js)
        producer.flush()
        '''
        time.sleep(1)
