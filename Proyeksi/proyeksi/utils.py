import json

import numpy as np
from keras import backend as K
from keras.callbacks import Callback


class Config:
    def __init__(self):
        pass


def set_config(config_dict):
    config = Config()
    config.__dict__ = config_dict
    return config


def root_mean_squared_error(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))


def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\n"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    return f'\r{prefix} |{bar}| {percent}% {suffix} {printEnd if iteration == total else ""}'


class CustomCallback(Callback):
    def __init__(self, websocket, config, batch_train_length, batch_test_length, dataset_train):
        self.websocket = websocket
        self.config = config
        self.batch_train_length = batch_train_length
        self.batch_test_length = batch_test_length
        self.dataset_train = dataset_train
        self.lr = config.learning_rate

    def on_train_begin(self, logs=None):
        self.websocket.send(text_data=json.dumps({
            'message': f'\nStarting Training with Tensor 3D (N, S, F) : ({self.batch_train_length} , {self.config.seq_len} , {self.dataset_train.shape[1]})\n'
        }))

    def on_train_end(self, logs=None):
        if self.config.max_epochs is not self.epoch:
            self.websocket.send(text_data=json.dumps({
                'message': f'Epoch {str(self.epoch)}: early stopping\n'
            }))
        self.websocket.send(text_data=json.dumps({
            'message': f'\nStop Training - loss: {round(logs["loss"], 5)} - val_loss: {round(logs["val_loss"], 5)}\n'
        }))

    def on_epoch_begin(self, epoch, logs=None):
        self.websocket.send(text_data=json.dumps({
            'message': f'\nStart Epoch {epoch + 1}/{self.config.max_epochs}\n'
        }))

    def on_epoch_end(self, epoch, logs=None):
        self.epoch = epoch + 1
        if self.lr > np.float32(logs["lr"]).item():
            self.lr = float(logs["lr"])
            self.websocket.send(text_data=json.dumps({
                'message': f'Epoch {epoch + 1}: reducing learning rate to {round(float(logs["lr"]), 10)}.\n'
            }))
        self.websocket.send(text_data=json.dumps({
            'message': f'End Epoch {epoch + 1}/{self.config.max_epochs} of training - loss: {round(logs["loss"], 5)} - val_loss: {round(logs["val_loss"], 5)} - lr: {round(float(logs["lr"]), 10)}\n'
        }))

    def on_train_batch_end(self, batch, logs=None):
        self.websocket.send(text_data=json.dumps({
            'message': progress_bar(batch, self.batch_train_length, prefix=f'Training Batch {str(batch)}/{str(self.batch_train_length)}', suffix=f'Complete - loss: {str(round(logs["loss"], 5))}', length=25)
        }))

    def on_test_batch_end(self, batch, logs=None):
        self.websocket.send(text_data=json.dumps({
            'message': progress_bar(batch, self.batch_test_length, prefix=f'Evaluating Batch {str(batch)}/{str(self.batch_test_length)}', suffix=f'Complete - loss: {str(round(logs["loss"], 5))}', length=25)
        }))
