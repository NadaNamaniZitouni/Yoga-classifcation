from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.preprocessing import image
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import numpy as np
from django.templatetags.static import static

# Load your deep learning model
model = load_model('C:/Users/louay/Desktop/Yoga/app/static/Yoga_classification.h5')
test=""

# Define function for preprocessing image before classification
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    #img_array = img_array / 255.0  # Scale pixel values to [0, 1]
    return img_array

# Define view function that handles image upload and classification
def classify_image(request):
    if request.method == 'POST':
        # Get uploaded image
        uploaded_image = request.FILES['image']
        # Save image to temporary location
        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        # Preprocess image
        processed_image = preprocess_image(fs.path(image_path))
        # Classify image using deep learning model
        predictions = model.predict(processed_image)
        # Get top prediction
        class_names =  {0:"downdog",1:"goddess",2:"mountain", 3:"tree", 4:"warrior1", 5:"warrior2"}
        top_prediction = class_names[np.argmax(predictions)]
        # Delete temporary image file
        fs.delete(image_path)
        # Render result to user
        return render(request, 'upload.html', {'prediction': top_prediction,'image': uploaded_image})
    else:
        # Render image upload form to user
        return render(request, 'upload.html',{'image':None})