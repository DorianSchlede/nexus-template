#!/bin/bash
#
# Docker test script for install.sh
# Tests the installer on Ubuntu container
#

set -e

echo "Building Docker test image..."
docker build -t nexus-installer-test -f 02-builds/03-one-command-installer/03-working/test-ubuntu.Dockerfile .

echo ""
echo "Running installer in Ubuntu container..."
docker run --rm -it nexus-installer-test

echo ""
echo "Docker test completed!"
