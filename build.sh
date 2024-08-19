# build.sh
#!/bin/bash

# Update package list and install the missing library
apt-get update && apt-get install -y libgl1-mesa-glx