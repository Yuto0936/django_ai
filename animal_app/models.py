from django.db import models
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
from PIL import Image
import io, base64


graph = tf.get_default_graph()

class Photo(models.Model):
    image = models.ImageField(upload_to='photos')

    classes = ['lion', 'tiger', 'cheetah']
    MODEL_FILE_PATH = './animal_app/ml_models/animal_cnn.h5'
    num_classes = len(classes)
    image_size = 50

    # 引数から画像ファイルを参照して読み込む
    def predict(self):
        image = None
        global graph
        with graph.as_default():
            model = load_model(self.MODEL_FILE_PATH)
            img_data = self.image.read()
            img_bin = io.BytesIO(img_data)
            image = Image.open(img_bin)
            image = image.convert('RGB')
            image = image.resize((self.image_size, self.image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            return self.classes[predicted], percentage
    

    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img