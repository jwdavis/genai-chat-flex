from vertexai.preview.vision_models import ImageGenerationModel
import re
import streamlit as st

def generate_image(prompt, empty, model_name="", parent=None):
    """
    Generates image based on the given prompt.

    Args:
        prompt (str): The prompt for generating the images.

    Returns:
        tuple: A tuple containing the generated images and any error that occurred during the generation process.
            The generated images are returned as a response.
            If an error occurs, it is returned as an error dictionary.
    """
    response = None
    error = None
    try:
        # consider implementing base_image
        model = ImageGenerationModel.from_pretrained("imagegeneration@006")
        with empty:
            with st.spinner("Generating Image..."):
                response = model.generate_images(
                    prompt=prompt,
                    number_of_images=1,
                    guidance_scale=21,
                    safety_filter_level="block_few",
                    person_generation="allow_adult",
                    aspect_ratio="1:1",
                )
        if response is None:
            return
        image = response.images[0]
        empty.image(image._image_bytes)
    except Exception as e:
        error = {"error": e}
        empty.json(e)
    return response, error
