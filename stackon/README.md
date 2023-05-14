# Stackedkon

## Objet

1. Mise en place d'un broker MQTT (Mosquitto) avec docker
2. Tests d'envoi et de réception de messages via le broker
3. Client python MQTT: worker: les "jobs" sont envoyés en ligne de commande
4. Gestion du multi-threading: un worker doit pouvoir gérer plusieurs jobs à la fois
5. TODO: Pour chaque job, utilisation de sous-threads/greenlets/etc.
6. Evolutions possibles: création d'un service d'enrichissement de données (catégo ?)

Architecture:
```
                                                                  pub/sub jobs/worker-1  ________
                                                                 -----------------------|worker-1|
 ______________  pub jobs/worker-$id    _______________________ /                        --------
|job-dispatcher|-----------------------|Mosquitto (MQTT broker)|
---------------  sub jobs/#             ----------------------- \                         ________
                                                                 ------------------------|worker-2|
                                                                  pub/sub jobs/worker-2   --------
```

## MQTT
(Message Queuing Telemetry Transport)
- TCP/IP
- typique pour IoT, peu de bande passante 
- pub: _publish_, envoyer un message (sur un topic)
- sub: _subscribe_, recevoir un message (sur un topic)

### Système de topics 
Organisation hiérarchique de _topics_ en partant d'une racine, comme pour des
répertoires. Exemples: 
```
/workers                        # on peut commencer par un "/"
workers                         # mais ça n'est pas obligé (et ce cas est plus courant)

# topic
workers                         # le topic workers
workers/scrapers                # scrapers

workers/#                       # tous les "workers": tous les message qui respectent la hiérarchie "workers"
workers/+                       # tous les "workers": tous les message qui respectent la hiérarchie "workers/"
workers/scrapers/#              # tous les "scrapers"
workers/data/#                  # tous les workers de "data"

workers/scrapers/scraper-1      # les données correspondant au scraper-1
```

## Architecture

- subscribe on `client`: receive
```
mosquitto_pub -m '{"task":"iter_acc","gid":"123"}' -t "workerpy/worker-1/job"
```

## Evolutions

```
                                                                  pub/sub jobs/worker-1 
                                                                  pub data/scrapers/worker-1   ________
                                                                 ----------------------------|worker-1|
 ______________  pub jobs/worker-$id    _______________________ /                             --------
|job-dispatcher|-----------------------|Mosquitto (MQTT broker)|
---------------  sub jobs/#             ----------------------- \                         ________
                                                |                ------------------------|worker-2|
                                                |                 pub/sub jobs/worker-2   --------
                                                |
                                            sub | data/scrapers/#
                                            pub | data/processed
                                        ________|__________________
                                       |data processor microservice|
                                        ---------------------------
```
