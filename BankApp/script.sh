#!/bin/bash

# Create the main project directory
mkdir bank_management_system
cd bank_management_system

# Create the project directory
django-admin startproject bank_management_system

# Navigate to the project directory
cd bank_management_system

# Create the Django apps directory
mkdir accounts banks transactions

# Create the migrations directory for each app
for app in accounts banks transactions; do
    mkdir $app/migrations
done

# Create __init__.py files for each app
touch accounts/__init__.py
touch banks/__init__.py
touch transactions/__init__.py

# Create files for the main project directory
touch manage.py
touch bank_management_system/__init__.py
touch bank_management_system/settings.py
touch bank_management_system/urls.py
touch bank_management_system/wsgi.py

# Create files for each app
for app in accounts banks transactions; do
    touch $app/admin.py
    touch $app/models.py
    touch $app/views.py
    touch $app/urls.py
done

# Create templates directory and subdirectories
mkdir templates
mkdir templates/accounts templates/banks templates/transactions

# Create HTML template files
touch templates/base.html
touch templates/accounts/login.html
touch templates/accounts/register.html
touch templates/banks/bank_list.html
touch templates/banks/bank_detail.html
touch templates/transactions/transaction_list.html
touch templates/transactions/transaction_detail.html

# Create static directory and subdirectories
mkdir static
mkdir static/css static/js static/img

# Output directory structure
echo "Directory structure created:"
tree .
