from .bootstrapping import from_project_root
import yaml

with open(from_project_root("flask_app", "app.yml")) as f:
    APP_NAME = yaml.load(f)["app_name"]
