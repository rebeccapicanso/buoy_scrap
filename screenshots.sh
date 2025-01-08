#!/bin/bash

SCREENSHOT_DIR="$HOME/Desktop  # Adjust this path as needed
OUTPUT_FILE="overlay_result.png"

# Check if directory exists
if [ ! -d "$SCREENSHOT_DIR" ]; then
    echo "Error: Screenshot directory not found at $SCREENSHOT_DIR"
    exit 1
fi

IMAGE_FILES=($(find "$SCREENSHOT_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \)))

if [ ${#IMAGE_FILES[@]} -eq 0 ]; then
    echo "No image files found in $SCREENSHOT_DIR"
    exit 1
fi

cp "${IMAGE_FILES[0]}" "$OUTPUT_FILE"

for ((i=1; i<${#IMAGE_FILES[@]}; i++)); do
    ffmpeg -i "$OUTPUT_FILE" -i "${IMAGE_FILES[$i]}" \
        -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[overlay];[0:v][overlay]overlay=0:0" \
        -y "temp_$OUTPUT_FILE"
    mv "temp_$OUTPUT_FILE" "$OUTPUT_FILE"
done

echo "Overlay complete! Result saved as $OUTPUT_FILE"