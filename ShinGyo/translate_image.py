from google.cloud import vision
from google.cloud import translate_v2 as translate

def extract_text_from_image(image_path):
    """Extract text from an image using the Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    text = response.full_text_annotation.text
    return text

def translate_text(text, target_language='es'):
    """Translate text using the Google Cloud Translation API."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    translated_text = result['translatedText']
    return translated_text

def main():
    image_path = "Downloads/FmvznfBaMAAGj6t.jpg"
    text = extract_text_from_image(image_path)
    translated_text = translate_text(text)
    print(translated_text)

if __name__ == "__main__":
    main()