#!/bin/bash
pip3 install -r requirements.txt
python3 manage.py collectstatic --settings=BlackboardCompanion.settings.prod --noinput
python3 manage.py migrate --settings=BlackboardCompanion.settings.prod