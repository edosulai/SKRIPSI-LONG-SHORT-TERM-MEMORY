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
