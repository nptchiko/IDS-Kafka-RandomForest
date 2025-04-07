#!/bin/bash

# Define the project root directory
PROJECT_NAME="."

# Create main project directories
#mkdir -p $PROJECT_NAME/{app/{static/{css,js,images},templates/{auth},blueprints/auth,instance},migrations,tests}
mkdir -p $PROJECT_NAME/{app/{static/{css,js,images},templates},}
# Create core Flask files
# touch $PROJECT_NAME/{run.py,wsgi.py,config.py,requirements.txt,.gitignore,.env,README.md}
touch $PROJECT_NAME/{run.py,config.py}

# Create Flask app structure
#touch $PROJECT_NAME/app/{__init__.py,routes.py,models.py,forms.py,services.py,extensions.py,error_handlers.py}

# Create blueprint files
#touch $PROJECT_NAME/app/blueprints/auth/{__init__.py,routes.py,models.py,forms.py}

# Create template files
touch $PROJECT_NAME/app/templates/{layout.html,index.html}
touch $PROJECT_NAME/app/templates/{login.html,register.html}

# Create test files
#touch $PROJECT_NAME/tests/{__init__.py,test_routes.py,test_models.py,test_forms.py}

# Create instance configuration
#touch $PROJECT_NAME/app/instance/config.py

# Write content to important files
# echo "from flask import Flask\n\ndef create_app():\n    app = Flask(__name__)\n    app.config.from_object('config.DevelopmentConfig')\n    return app" >$PROJECT_NAME/app/__init__.py
#
# echo "SECRET_KEY='your_secret_key'\nDEBUG=True" >$PROJECT_NAME/.env
#
# echo "__pycache__/\ninstance/\n.env\n*.pyc\n*.pyo\n*.db\n*.sqlite3" >$PROJECT_NAME/.gitignore
#
# echo "class DevelopmentConfig:\n    DEBUG = True\n    SECRET_KEY = 'dev_secret_key'\n\nclass ProductionConfig:\n    DEBUG = False\n    SECRET_KEY = 'prod_secret_key'" >$PROJECT_NAME/config.py
#
# echo "from app import create_app\n\napp = create_app()\n\nif __name__ == '__main__':\n    app.run(debug=True)" >$PROJECT_NAME/run.py
#
# echo "from app import create_app\n\napp = create_app()\n\nif __name__ == '__main__':\n    app.run()" >$PROJECT_NAME/wsgi.py
#
# echo "Flask Web Application" >$PROJECT_NAME/README.md
#
# echo -e "flask\nflask-sqlalchemy\nflask-wtf\nflask-login\nflask-migrate" >$PROJECT_NAME/requirements.txt
#
# echo "Project structure created successfully!"
