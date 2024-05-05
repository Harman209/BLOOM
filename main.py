from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("/content/Dr-Leaf/models/keras_model.h5", compile=False)

# Load the labels
class_names = open("/content/Dr-Leaf/models/labels.txt", "r").readlines()

def prediction(image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # resizing the image to be at least 224x224 and then cropping from the center
    image_PIL = Image.fromarray(image)
    size = (224, 224)
    image = ImageOps.fit(image_PIL, size, Image.ANTIALIAS)
    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return class_name[2:], confidence_score*100

import gradio

gui = gradio.Interface(fn=prediction, inputs="image", outputs= gradio.Textbox(label="status"), title="Dr. Leaf", description="A model to predict the disease of a plant")
gui.launch(share=True)

