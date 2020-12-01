## Usage:
Add to configuration.yaml:

please remember to add bbk_cli to the directory. (I'm running in docker and I have /config as a volume in the docker to have it persisted) 

```
sensor:
  - platform: bredbandskollen
    path: /config/deps/bbk_cli
```
