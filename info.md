## Usage:
Add to configuration.yaml:

please remember to add bbk_cli to the directory. (I'm running in docker and I have /config as a volume in the docker to have it persisted) 

```
sensor:
  - platform: bredbandskollen
    path: /config/deps/bbk_cli
```

if you are running in a docker, you probably need to compile it manually once

if the repo of dotse is not updated you can use my fork wich have a fix to make it build

git clone https://github.com/benganellison/bbk.git

```
sudo docker exec -it -u root home-assistant sh
cd /config
mkdir deps
cd deps
git clone https://github.com/dotse/bbk.git
cd bbk/src/cli
apk add build-base
make
mv cli /config/deps/bbk_cli
cd /config/deps
rm -R bbk
```
