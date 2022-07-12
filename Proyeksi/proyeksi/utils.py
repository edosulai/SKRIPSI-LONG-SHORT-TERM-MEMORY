import json

import numpy as np
import tensorflow as tf


class Config:

    def __init__(self):
        pass


def set_config(config_dict):
    config = Config()
    config.__dict__ = config_dict
    return config


def mean_squared_error(y_true, y_pred):
    return tf.keras.backend.mean(tf.keras.backend.square(y_pred - y_true))


def root_mean_squared_error(y_true, y_pred):
    return tf.keras.backend.sqrt(mean_squared_error(y_pred, y_true))


def progress_bar(iteration,
                 total,
                 prefix='',
                 suffix='',
                 decimals=1,
                 length=100,
                 fill='█',
                 printEnd="\n"):
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return f'\r{prefix} |{bar}| {percent}% {suffix} {printEnd if iteration == total else ""}'


def train_test_split(dataset, timestep=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - timestep):
        dataX.append(dataset[i:(i + timestep)])
        dataY.append(dataset[i + timestep:i+timestep+1])
    return np.array(dataX), np.array(dataY)

def proyeksi_split(dataset, timestep=1):
    dataX = []
    for i in range(len(dataset) - timestep + 1):
        dataX.append(dataset[i:(i + timestep)])
    return np.array(dataX)

# class CustomCallback(tf.keras.callbacks.Callback):

#     def __init__(self, websocket, X_train, X_test, config):
#         self.websocket = websocket
#         self.X_train = X_train
#         self.X_test = X_test
#         self.lr = config.learning_rate
#         self.sequence_len = config.timestep
#         self.feature_len = len(config.feature)
#         self.max_epoch = config.max_epoch
#         self.logs = config.logs

#     def on_train_begin(self, logs=None):
#         self.websocket.send(text_data=json.dumps({
#             'message':
#             f'\nStarting Training with Tensor 3D (Batch Size, Feature, Timestep Length) : ({self.X_train.shape[0]} , {self.feature_len} , {self.sequence_len})\n'
#         }))

#     def on_train_end(self, logs=None):
#         self.websocket.send(text_data=json.dumps({
#             'message':
#             f'\nStop Training - loss: {round(logs["loss"], 5)}\n\n'
#         }))

#     def on_epoch_begin(self, epoch, logs=None):
#         self.websocket.send(text_data=json.dumps({
#             'message': f'\nStart Epoch {epoch + 1}/{self.max_epoch}\n'
#         }))

#     def on_epoch_end(self, epoch, logs=None):
#         self.websocket.send(text_data=json.dumps({
#             'message':
#             f'End Epoch {epoch + 1}/{self.max_epoch} of training - loss: {round(logs["loss"], 5)}\n'
#         }))

#     def on_train_batch_end(self, batch, logs=None):
#         self.websocket.send(text_data=json.dumps({
#             'message':
#             progress_bar(
#                 batch + 1,
#                 self.X_train.shape[0],
#                 prefix=
#                 f'Training Batch {str(batch)}/{str(self.X_train.shape[0])}',
#                 suffix=f'Completed - loss: {str(round(logs["loss"], 5))}',
#                 length=25
#             )
#         }))

#     def on_test_batch_end(self, batch, logs=None):
#         self.websocket.send(text_data=json.dumps({
#             'message':
#             progress_bar(
#                 batch + 1,
#                 self.X_test.shape[0],
#                 prefix=
#                 f'Evaluating Batch {str(batch)}/{str(self.X_test.shape[0])}',
#                 suffix=f'Completed - loss: {str(round(logs["loss"], 5))}',
#                 length=25
#             )
#         }))
