# OpenModex Visualization

[! https://img.shields.io/github/license/your_github_username/openmodex-visualization] [! https://img.shields.io/badge/Made%20at-Starschema-red]
A short description of the project.


## Running locally

To run a development instance locally, create a virtualenv, install the 
requirements from `requirements.txt` and launch `app.py` using the 
Python executable from the virtualenv.

## Running locally with docker:

```
sudo docker-compose -f local.yml run --rm -e MANAGE_DB=True modex_visualization python manage.py
sudo docker-compose -f local.yml up -d --build
```

## Deploying on ECS

Use `make image` to create a Docker image. Then, follow [these 
instructions](https://www.chrisvoncsefalvay.com/2019/08/28/deploying-dash-on-amazon-ecs/) 
to deploy the image on ECS.