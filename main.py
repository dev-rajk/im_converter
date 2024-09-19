import os
import logging
from io import BytesIO
from PIL import Image
from pillow_heif import register_heif_opener
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Register HEIC format opener for Pillow
register_heif_opener()

# Function to convert HEIC to JPG and return the converted image in memory
def convert_heic_to_jpg(image, output_quality=50):
    """
    Converts a HEIC image to JPG format.
    
    Args:
        image: Image file in HEIC format.
        output_quality (int): Quality of the output JPG image (1-100).
    
    Returns:
        A BytesIO object containing the JPG image data.
    """
    with Image.open(image) as img:
        # Convert and save the image in memory (to BytesIO)
        jpg_image = BytesIO()
        img.save(jpg_image, format="JPEG", quality=output_quality)
        jpg_image.seek(0)
        return jpg_image

# Function to display image metadata
def display_image_metadata(image):
    """
    Display metadata of the image.
    
    Args:
        image: Image object opened using PIL.
    """
    st.write(f"**Format:** {image.format}")
    st.write(f"**Size (width x height):** {image.size}")
    st.write(f"**Mode:** {image.mode}")

# Streamlit UI

st.title("HEIC to JPG Converter")

# File uploader allowing up to 5 HEIC images
uploaded_files = st.file_uploader(
    "Upload HEIC images (max 5)", type=['heic'], accept_multiple_files=True
)

# Slider to adjust output JPG quality
output_quality = st.slider("Select JPG Output Quality:", min_value=1, max_value=100, value=80)

if uploaded_files:
    # Loop through each uploaded file
    for uploaded_file in uploaded_files:
        # Convert HEIC to JPG
        st.subheader(f"Original HEIC File: {uploaded_file.name}")
        
        # Display HEIC image and its metadata
        with Image.open(uploaded_file) as img:
            st.image(img, caption="HEIC Image", use_column_width=True)
            display_image_metadata(img)

        # Convert the HEIC image to JPG
        jpg_image = convert_heic_to_jpg(uploaded_file, output_quality)

        # Display the converted JPG image
        st.subheader(f"Converted JPG: {uploaded_file.name}")
        st.image(jpg_image, caption="Converted JPG Image", use_column_width=True)

        # Provide download button for the JPG image
        st.download_button(
            label="Download JPG",
            data=jpg_image,
            file_name=uploaded_file.name.replace('.heic', '.jpg'),
            mime='image/jpeg'
        )
