import os
from PIL import Image
import numpy as np
from curator import DQNAgent, ColorEnvironment, load_images
from image_assistant import prep, prioritize_colors, analyze_image, get_dominant_color, preprocess_image

def sort_images_by_color(agent, image_directory):
    images = load_images(image_directory)
    sorted_images = []
    
    for image_path in images:
        img = preprocess_image(image_path)
        action = agent.act(img)  # Predict the dominant color
        
        # Additional analysis
        contains_moon, is_night = analyze_image(image_path)
        dominant_color = get_dominant_color(image_path)
        
        sorted_images.append((image_path, action, contains_moon, is_night, dominant_color))
    
    # Sort images based on the predicted color and other criteria
    sorted_images.sort(key=lambda x: (x[1], x[2], x[3], x[4]))
    
    return sorted_images

def curate_images(sorted_images, criteria):
    curated_images = []
    for image_path, _, contains_moon, is_night, dominant_color in sorted_images:
        image_parts = prep(image_path)
        colors = [get_dominant_color(part) for part in image_parts]
        prioritized_colors = prioritize_colors(colors, criteria)
        
        # Simple curation logic (you can expand this)
        if contains_moon and is_night:
            curated_images.append((image_path, "Night sky with moon"))
        elif prioritized_colors[0] == dominant_color:
            curated_images.append((image_path, "Harmonious color composition"))
    
    return curated_images

def main():
    # Train the model (you might want to do this separately and save the model)
    from curator import main as train_curator
    trained_agent = train_curator()
    
    # Directory containing the images you want to sort
    image_directory = "path/to/your/unsorted/images"
    
    # Sort the images
    sorted_images = sort_images_by_color(trained_agent, image_directory)
    
    # Define curation criteria (example values, adjust as needed)
    curation_criteria = {
        'brightness': 0.7,
        'saturation': 0.5,
        'hue_preference': 0.3
    }
    
    # Curate the images
    curated_images = curate_images(sorted_images, curation_criteria)
    
    # Print or use the curated images as needed
    for image_path, reason in curated_images:
        print(f"Curated Image: {image_path}, Reason: {reason}")

if __name__ == "__main__":
    main()