# -*- coding: utf-8 -*-
"""submission.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q8vm3VY0trVzvOaXbYGBb4QnrYQKtkYf
"""

import tensorflow as tf
import os, zipfile
import splitfolders
from tensorflow.keras.preprocessing.image import ImageDataGenerator

!wget --no-check-certificate \
 https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip \
  -O /tmp/rockpaperscissors.zip

local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

# membagi direktori foto menjadi 2 direktori untuk direktori pelatihan dan validasi 
base_dir = '/tmp/rockpaperscissors/rps-cv-images/base'
if 'base' not in os.listdir('/tmp/rockpaperscissors/rps-cv-images'):
  splitfolders.ratio('/tmp/rockpaperscissors/rps-cv-images', output='base_dir', seed=1337, ratio=(.6, .4))

# membuat direktori train dan validation
train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'val')

# Membuat direktori train dan validation di masing2 direktori rock, paper, scissors
rock_train_dir, rock_val_dir = os.path.join(train_dir, 'rock'), os.path.join(val_dir, 'rock')
paper_train_dir, paper_val_dir = os.path.join(train_dir, 'paper'), os.path.join(val_dir, 'paper')
scissors_train_dir, scissors_val_dir = os.path.join(train_dir, 'scissors'), os.path.join(val_dir, 'scissors')

train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range=0.2,
                    zoom_range=0.2,
                    fill_mode='nearest')
 
val_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    horizontal_flip=True,
                    shear_range = 0.2,
                    zoom_range=0.2,
                    fill_mode = 'nearest')

# menghasilkan data baru berdasarkan atribut yg sudah ditetukan
train_generator = train_datagen.flow_from_directory(
        train_dir,  # direktori data latih
        target_size=(150, 150),
        batch_size=41,
        class_mode='categorical')
 
validation_generator = val_datagen.flow_from_directory(
        val_dir, # direktori data validasi
        target_size=(150, 150),
        batch_size=41,
        class_mode='categorical')

# Membuat Model CNN
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer=tf.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# melatih model
model.fit(
      train_generator,
      steps_per_epoch=25,
      epochs=15,
      validation_data=validation_generator,
      validation_steps=5,
      verbose=2)

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  
  print(fn)
  print(classes)
if classes[0][0] == 1:
  print('It\'s a Rock!')
elif classes[0][1] == 1:
  print('It\'s a Paper!')
elif classes[0][2] == 1:
  print('It\'s a Scissors!')

"""*   Nama: Muhammad Sabil Ghina
*   Domisili: Jakarta Barat
*   E-mail: muhammadsabil333@gmail.com
*   Username: allein56
*   Pendidikan: Strata-1, Prodi Teknologi Industri Pertanian UNPAD
"""