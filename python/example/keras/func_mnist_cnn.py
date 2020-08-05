from flexflow.keras.models import Model, Sequential
from flexflow.keras.layers import Input, Flatten, Dense, Activation, Conv2D, MaxPooling2D, Concatenate, concatenate
import flexflow.keras.optimizers
from flexflow.keras.datasets import mnist
from flexflow.keras.datasets import cifar10
from flexflow.keras import losses
from flexflow.keras import metrics
from flexflow.keras.callbacks import Callback, VerifyMetrics
from example.accuracy import ModelAccuracy

import flexflow.core as ff
import numpy as np
import argparse
import gc
  
def top_level_task():
  num_classes = 10

  img_rows, img_cols = 28, 28
  
  (x_train, y_train), (x_test, y_test) = mnist.load_data()
  x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
  
  x_train = x_train.astype('float32')
  x_train /= 255
  y_train = y_train.astype('int32')
  y_train = np.reshape(y_train, (len(y_train), 1))
  
  input_tensor = Input(shape=(1, 28, 28), dtype="float32")
  
  output = Conv2D(filters=32, input_shape=(1,28,28), kernel_size=(3,3), strides=(1,1), padding=(1,1), activation="relu")(input_tensor)
  output = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding=(1,1), activation="relu")(output)
  output = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding="valid")(output)
  output = Flatten()(output)
  output = Dense(128, activation="relu")(output)
  output = Dense(num_classes)(output)
  output = Activation("softmax")(output)

  model = Model(input_tensor, output)
  
  opt = flexflow.keras.optimizers.SGD(learning_rate=0.001)
  model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy', 'sparse_categorical_crossentropy'])
  
  print(model.summary())
  
  flatten1 = model.get_layer(name='flat')
  t1 = flatten1.output_tensors[0]
  t2 = flatten1.input_tensors[0]
  print("t1: ", t1.to_layers, " ", t1.from_layer)
  print("t2: ", t2.to_layers, " ", t2.from_layer)
  
  model.fit(x_train, y_train, epochs=1, callbacks=[VerifyMetrics(ModelAccuracy.MNIST_CNN)])

if __name__ == "__main__":
  print("Functional API, mnist cnn")
  top_level_task()
  gc.collect()