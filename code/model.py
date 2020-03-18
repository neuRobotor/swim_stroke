import tensorflow as tf
import keras
from tensorflow.keras import Model, Input, Sequential
from tensorflow.keras.layers import Reshape, Conv1D, Conv2D, Activation, MaxPool2D, Flatten, Dropout, Dense, \
    Convolution1D, GlobalAveragePooling1D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard
import pandas as pd
import numpy as np
import time
from utils import window_process, visulization_results

cate_list = ['unknown', 'freestyle', 'breaststroke', 'butterfly', 'backstroke']

# train_path = r'../train_data/merged.csv'
train_path = r'F:/wangpengfei/泳姿/swimming_stroke/swimming/data/processed/train_1_V2.csv'

# train_file = pd.read_csv(train_path)
# print(train_file.head())
# print(train_file.columns.values[0:193])
#
# train_data = train_file[train_file.columns.values[1:10]]
#
# train_label = train_file[train_file.columns.values[10]].tolist()

# train_file = pd.get_dummies(data=train_file, prefix='species')

# print("train data:\n", train_data.describe())
# print("train label:\n", train_label)
# print(train_label.head())

# train_data_df = pd.DataFrame(train_data)

model = Sequential()
input_shape = (90, 6, 1)
# C1
model.add(Conv2D(filters=6, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
# model.add(MaxPool2D(3))
# C2
model.add(Conv2D(filters=6, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPool2D(3))
# C3
model.add(Conv2D(filters=6, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPool2D(3))
# C4
model.add(Conv2D(filters=6, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPool2D(3))

model.add(Flatten())
# Fully-connected
model.add(Dense(12, activation='relu'))
model.add(Dense(len(cate_list), activation='softmax'))
model.summary()

# train_label = np_utils.to_categorical(train_label, len(cate_list))
train_data, train_label = window_process.process_data(train_path)

print('train_shape: ', train_data.shape)
# train_data = tf.constant(train_data, shape=[22, 180, 6, 1])
# train_data = np.expand_dims(train_data, axis=-1)
train_label = to_categorical(train_label, len(cate_list))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=[tf.keras.metrics.categorical_accuracy, 'mse'])

# train_data = np_utils.to_categorical(train_data, 34)
# print(train_data)

model_path = '../model/20200318_{}.h5'.format(int(time.strftime('%Y%m%d%H%M', time.localtime(time.time()))))

cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=model_path,
    verbose=1,
    save_best_only=True,
)

result = model.fit(train_data,
                   train_label,
                   batch_size=500,
                   callbacks=[cp_callback],
                   validation_split=0.25,
                   epochs=2)

visulization_results.draw_result(result)
