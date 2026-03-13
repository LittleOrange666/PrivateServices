#!/bin/bash
export image_name="littleorange666/private_services"
if [ -z $1 ]; then
  echo "version is required for the release build"
  echo "Usage: $0 <version>"
else
  echo "Building version $1"
  docker build . -t $image_name:$1 | exit 1
  echo "Pushing version $1"
  docker push $image_name:$1
  echo "Building latest"
  docker build . -t $image_name:latest | exit 1
  echo "Pushing latest"
  docker push $image_name:latest
fi