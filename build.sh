#!/bin/bash

# Set executable permission for the script itself
chmod +x build.sh

# Install the missing library
apt-get update && apt-get install -y libgl1-mesa-glx
