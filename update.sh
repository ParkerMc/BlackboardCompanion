#!/bin/bash
sudo systemctl stop blackboard_companion.service
git pull
./setup.sh
sudo systemctl start blackboard_companion.service