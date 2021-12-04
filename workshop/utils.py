"""Workshop utils."""
# Standard Library
import base64


def encode_image_to_base64(image):
    """Encode image to base64."""
    encoded = base64.b64encode(image).decode('utf-8')
    return f'data:image/png;base64,{encoded}'
