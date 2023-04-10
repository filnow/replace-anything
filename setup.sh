#!/bin/bash

# Check if the script was invoked with an argument
if [ $# -eq 0 ]; then
  echo "Please specify a model variant: vit_h, vit_l, or vit_b"
  exit 1
fi

# Download the appropriate model variant based on the argument
case "$1" in
  vit_h)
    MODEL_URL="https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
    ;;
  vit_l)
    MODEL_URL="https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth"
    ;;
  vit_b)
    MODEL_URL="https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
    ;;
  *)
    echo "Invalid model variant: $1. Please specify vit_h, vit_l, or vit_b."
    exit 1
    ;;
esac

# Create the model directory if it doesn't already exist
if [ ! -d "./model" ]; then
  mkdir "./model"
fi

# Download the model file and move it to the model directory
curl "$MODEL_URL" --output "./model/sam_$1.pth"

# Install the required dependencies using pip
pip install -r requirements.txt
