# skin-tool-python

A python opencv application that generates variants of minecraft skins

# How to use

Python dependency management sucks, but thankfully we've docker. With docker installed on your system, do:

```bash
bash scripts/build-container.sh && bash scritps/run-container.sh
```

And you should've a container running on port 8080. To generate the skins just make an http request to

```http
GET localhost:8080/<minecraft_name>.
```
