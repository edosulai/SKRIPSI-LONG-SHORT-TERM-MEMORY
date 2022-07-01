from tkinter import E
from channels.generic.websocket import WebsocketConsumer

from proyeksi.models import Klimatologi

import json
import math

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# from datetime import datetime, timedelta

# from keras.callbacks import EarlyStopping, ReduceLROnPlateau


# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM
# from keras.layers import Dropout
# from keras.optimizers import adam_v2

from proyeksi.utils import set_config, mean_squared_error, root_mean_squared_error, train_test_split, CustomCallback

# Create your consumers here.


class ProyeksiConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        try:
            klimatologi_data = Klimatologi.objects.all()
            text_data_json = json.loads(text_data)
            config = set_config({
                "timestep": int(text_data_json['timestep']),
                "max_epoch": int(text_data_json['max_epoch']),
                "max_batch_size": int(text_data_json['max_batch_size']),
                "layer_size": int(text_data_json['layer_size']),
                "unit_size": int(text_data_json['unit_size']),
                "learning_rate": float(text_data_json['learning_rate']),
                "dropout": float(text_data_json['dropout']),
                'row_start': text_data_json['row_start'],
                'row_end': text_data_json['row_end'],
                'num_predict': int(text_data_json['num_predict']),
                "time_col": 'tanggal',
                "feature": ['rr']
            })

            dataset = pd.DataFrame(list(klimatologi_data.values())).replace(to_replace=[8888, 9999, 2555], value=np.nan)
            dataset.interpolate(inplace=True)

            datelist = list(dataset[config.time_col])
            featureset = dataset[config.feature]
            vector_featureset = featureset.values

            self.send(text_data=json.dumps({
                'message': f'Dataset Shape : {featureset.shape}\nFeatured Selected: : {config.feature}\nPredict Selected: : {config.feature}\n'
            }))

            scaller = MinMaxScaler()
            vector_featureset_scaled = scaller.fit_transform(vector_featureset)

            train_size = int(vector_featureset_scaled.size * 0.9)
            trainset, testset = vector_featureset_scaled[0:train_size], vector_featureset_scaled[train_size:vector_featureset_scaled.size]

            X_train, y_train = train_test_split(trainset, time_step=config.timestep)
            X_test, y_test = train_test_split(testset, time_step=config.timestep)

            X_train = np.reshape(X_train, (X_train.shape[0], len(config.feature), X_train.shape[1]))
            X_test = np.reshape(X_test, (X_test.shape[0], len(config.feature), X_test.shape[1]))
            
            self.send(text_data=json.dumps({
                'message': f'Input (X) Train Shape : {X_train.shape}\nLabel (Y) Train Shape : {y_train.shape}\n'
            }))

            # model = Sequential()
            # model.add(LSTM(units=config.hidden_size, return_sequences=True,
            #           input_shape=(n_past, dataset_train.shape[1]-1)))
            # model.add(LSTM(units=config.hidden_size, return_sequences=False))
            # model.add(Dropout(config.dropout))
            # model.add(Dense(units=config.output_size, activation='linear'))

            # model.compile(optimizer=adam_v2.Adam(
            #     learning_rate=config.learning_rate), loss=root_mean_squared_error)

            # es = EarlyStopping(monitor='val_loss',
            #                    min_delta=1e-10, patience=10, verbose=0)
            # rlr = ReduceLROnPlateau(
            #     monitor='val_loss', factor=0.5, patience=10, verbose=0)
            # custom = CustomCallback(
            #     websocket=self, config=config, batch_train_length=batch_train_length, batch_test_length=batch_test_length, dataset_train=dataset_train)

            # model.fit(x_train, y_train, shuffle=config.suffle, epochs=config.max_epochs, callbacks=[es, rlr, custom], validation_split=config.validation_split, verbose=0, batch_size=config.batch_size)

            # self.send(text_data=json.dumps({
            #     'message': f'\nStart predicting...\n'
            # }))
            # predictions_train = model.predict(x_train[n_past:], verbose=0)
            # predictions_future = model.predict(x_train[-n_future:], verbose=0)
            
            # self.send(text_data=json.dumps({
            #     'message': f'Plotting Datasets...\n'
            # }))

            # START_DATE_FOR_PLOTTING = (
            #     datelist_train[-1] - timedelta(days=max((config.much_day_predict - 1) * 3, 90))).strftime("%Y-%m-%d")

            # datelist_future = pd.date_range(
            #     datelist_train[-1], periods=n_future, freq='1d')

            # y_pred_future = sc_predict.inverse_transform(predictions_future)
            # y_pred_train = sc_predict.inverse_transform(predictions_train)

            # PREDICTIONS_FUTURE = pd.DataFrame(y_pred_future, columns=[
            #     config.prediction_col]).set_index(pd.Series(datelist_future))
            # PREDICTION_TRAIN = pd.DataFrame(y_pred_train, columns=[config.prediction_col]).set_index(
            #     pd.Series(datelist_train[2 * n_past + n_future - 1:]))
            # DATASET_TRAIN = pd.DataFrame(dataset_train, columns=columns_train).set_index(
            #     pd.Series(datelist_train))

            # PREDICTIONS_FUTURE.index = PREDICTIONS_FUTURE.index.to_series().apply(
            #     lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            # PREDICTION_TRAIN.index = PREDICTION_TRAIN.index.to_series().apply(
            #     lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            # DATASET_TRAIN.index = DATASET_TRAIN.index.to_series().apply(
            #     lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            
            # self.send(text_data=json.dumps({
            #     'message': f'...\n'
            # }))

            # self.send(text_data=json.dumps({
            #     'results': {
            #         'future': pd.DataFrame({
            #             "tanggal": [x.strftime('%d-%m-%Y') for x in PREDICTIONS_FUTURE.index],
            #             config.prediction_col: [
            #                 x for x in PREDICTIONS_FUTURE[config.prediction_col]]
            #         }).to_dict('records'),
            #         'train': pd.DataFrame({
            #             "tanggal": [x.strftime('%d-%m-%Y') for x in PREDICTION_TRAIN.loc[START_DATE_FOR_PLOTTING:].index],
            #             config.prediction_col: PREDICTION_TRAIN.loc[START_DATE_FOR_PLOTTING:][config.prediction_col].tolist(
            #             )
            #         }).to_dict('records'),
            #         'histori': pd.DataFrame({
            #             "tanggal": [x.strftime('%d-%m-%Y') for x in DATASET_TRAIN.loc[START_DATE_FOR_PLOTTING:].index],
            #             config.prediction_col: DATASET_TRAIN.loc[START_DATE_FOR_PLOTTING:][config.prediction_col].tolist(
            #             )
            #         }).to_dict('records'),
            #     }
            # }))

            self.close()
        except Exception as e:
            self.send(text_data=json.dumps({
                'message': f'Error : {e}\n'
            }))
            self.close()
