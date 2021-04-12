#!/bin/bash
pip3 install -r requirements.txt
python manage.py migrate --settings=BlackboardCompanion.settings.dev