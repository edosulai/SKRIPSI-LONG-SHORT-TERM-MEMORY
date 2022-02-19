from channels.generic.websocket import WebsocketConsumer

from proyeksi.models import Klimatologi

import json
import math

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from keras.callbacks import EarlyStopping, ReduceLROnPlateau

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.optimizers import adam_v2

from proyeksi.utils import set_config, root_mean_squared_error, CustomCallback

# Create your consumers here.


class ProyeksiConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            columns_train = ['tavg', 'rh_avg', 'rr', 'ff_avg']
            config = set_config({
                "input_size": columns_train.__len__(),
                "seq_len": int(text_data_json['sequence']),
                "batch_size": int(text_data_json['batch_size']),
                "output_size": 1,
                "hidden_size": int(text_data_json['hidden_units']),
                "num_layers": 2,
                "dropout": float(text_data_json['dropout']),
                "bidirectional": True,
                "learning_rate": float(text_data_json['learning_rate']),
                "max_epochs": int(text_data_json['max_epoch']),
                "time_col": 'tanggal',
                "prediction_col": columns_train[2],
                'much_day_predict': int(text_data_json['much_predict']) + 1,
                'nan_handling': int(text_data_json['nan_handling']),
                'validation_split': 0.1,
                'suffle': False,
            })
            usecols = [config.time_col] + columns_train

            dataset_train = pd.DataFrame(list(Klimatologi.objects.all().values(
            )), columns=usecols).replace(to_replace=[8888, 9999, 2555], value=np.nan)

            if config.nan_handling is 1:
                dataset_train.dropna(inplace=True)
            elif config.nan_handling is 2:
                dataset_train.interpolate(inplace=True)

            datelist_train = list(dataset_train[config.time_col])
            dataset_train = dataset_train[columns_train]
            training_set = dataset_train.values

            self.send(text_data=json.dumps({
                'message': f'Training Set Shape : {dataset_train.shape}\nFeatured Selected: : {columns_train}\nPredict Selected: : {config.prediction_col}\n'
            }))

            sc = MinMaxScaler()
            training_set_scaled = sc.fit_transform(training_set)

            sc_predict = MinMaxScaler()
            sc_predict.fit_transform(training_set[:, 2:3])

            x_train = []
            y_train = []

            n_future = config.much_day_predict
            n_past = config.seq_len

            for i in range(n_past, len(training_set_scaled) - n_future + 1):
                x_train.append(
                    training_set_scaled[i - n_past:i, 0:dataset_train.shape[1] - 1])
                y_train.append(
                    training_set_scaled[i + n_future - 1:i + n_future, 2])

            x_train, y_train = np.array(x_train), np.array(y_train)

            batch_train_length = math.floor(
                (y_train.__len__()*(1-config.validation_split))/config.batch_size)
            batch_test_length = math.floor(
                (y_train.__len__()*config.validation_split)/config.batch_size)

            self.send(text_data=json.dumps({
                'message': f'X Train Shape : {x_train.shape}\nY Train Shape : {y_train.shape}\n'
            }))

            model = Sequential()
            model.add(LSTM(units=config.hidden_size, return_sequences=True,
                      input_shape=(n_past, dataset_train.shape[1]-1)))
            model.add(LSTM(units=config.hidden_size, return_sequences=False))
            model.add(Dropout(config.dropout))
            model.add(Dense(units=config.output_size, activation='linear'))

            model.compile(optimizer=adam_v2.Adam(
                learning_rate=config.learning_rate), loss=root_mean_squared_error)

            es = EarlyStopping(monitor='val_loss',
                               min_delta=1e-10, patience=10, verbose=0)
            rlr = ReduceLROnPlateau(
                monitor='val_loss', factor=0.5, patience=10, verbose=0)
            custom = CustomCallback(
                websocket=self, config=config, batch_train_length=batch_train_length, batch_test_length=batch_test_length, dataset_train=dataset_train)

            model.fit(x_train, y_train, shuffle=config.suffle, epochs=config.max_epochs, callbacks=[es, rlr, custom], validation_split=config.validation_split, verbose=0, batch_size=config.batch_size)

            self.send(text_data=json.dumps({
                'message': f'\nStart predicting...\n'
            }))
            predictions_train = model.predict(x_train[n_past:], verbose=0)
            predictions_future = model.predict(x_train[-n_future:], verbose=0)
            
            self.send(text_data=json.dumps({
                'message': f'Plotting Datasets...\n'
            }))

            START_DATE_FOR_PLOTTING = (
                datelist_train[-1] - timedelta(days=max((config.much_day_predict - 1) * 3, 90))).strftime("%Y-%m-%d")

            datelist_future = pd.date_range(
                datelist_train[-1], periods=n_future, freq='1d')

            y_pred_future = sc_predict.inverse_transform(predictions_future)
            y_pred_train = sc_predict.inverse_transform(predictions_train)

            PREDICTIONS_FUTURE = pd.DataFrame(y_pred_future, columns=[
                config.prediction_col]).set_index(pd.Series(datelist_future))
            PREDICTION_TRAIN = pd.DataFrame(y_pred_train, columns=[config.prediction_col]).set_index(
                pd.Series(datelist_train[2 * n_past + n_future - 1:]))
            DATASET_TRAIN = pd.DataFrame(dataset_train, columns=columns_train).set_index(
                pd.Series(datelist_train))

            PREDICTIONS_FUTURE.index = PREDICTIONS_FUTURE.index.to_series().apply(
                lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            PREDICTION_TRAIN.index = PREDICTION_TRAIN.index.to_series().apply(
                lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            DATASET_TRAIN.index = DATASET_TRAIN.index.to_series().apply(
                lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            
            self.send(text_data=json.dumps({
                'message': f'...\n'
            }))

            self.send(text_data=json.dumps({
                'results': {
                    'future': pd.DataFrame({
                        "tanggal": [x.strftime('%d-%m-%Y') for x in PREDICTIONS_FUTURE.index],
                        config.prediction_col: [
                            x for x in PREDICTIONS_FUTURE[config.prediction_col]]
                    }).to_dict('records'),
                    'train': pd.DataFrame({
                        "tanggal": [x.strftime('%d-%m-%Y') for x in PREDICTION_TRAIN.loc[START_DATE_FOR_PLOTTING:].index],
                        config.prediction_col: PREDICTION_TRAIN.loc[START_DATE_FOR_PLOTTING:][config.prediction_col].tolist(
                        )
                    }).to_dict('records'),
                    'histori': pd.DataFrame({
                        "tanggal": [x.strftime('%d-%m-%Y') for x in DATASET_TRAIN.loc[START_DATE_FOR_PLOTTING:].index],
                        config.prediction_col: DATASET_TRAIN.loc[START_DATE_FOR_PLOTTING:][config.prediction_col].tolist(
                        )
                    }).to_dict('records'),
                }
            }))

            self.close()
        except Exception as e:
            print(e)
            self.close()
