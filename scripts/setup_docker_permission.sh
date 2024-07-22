#!/bin/bash

sudo usermod -aG docker $USER
newgrp docker
groups
sudo systemctl restart docker