from tkinter import E
from channels.generic.websocket import WebsocketConsumer

from proyeksi.models import Klimatologi, Riwayat

import json
import math
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

from proyeksi.utils import set_config, mean_squared_error, root_mean_squared_error, train_test_split, proyeksi_split, progress_bar, CustomCallback

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
                "feature": text_data_json['feature_training'],
                "prediction": text_data_json['feature_predict'],
                "logs": []
            })
            
            self.send(text_data=json.dumps({
                'message': json.dumps({
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
                "feature": text_data_json['feature_training'],
                "prediction": text_data_json['feature_predict'],
                "logs": []
            })
            }))

            # DATASETS = pd.DataFrame(list(klimatologi_data.values())).replace(to_replace=[8888, 9999, 2555], value=np.nan)
            # DATASETS = DATASETS.loc[
            #     (pd.to_datetime(DATASETS[config.time_col]) >= datetime.strptime(config.row_start.strip(), '%Y-%m-%d')) & 
            #     (pd.to_datetime(DATASETS[config.time_col]) <= datetime.strptime(config.row_end.strip(), '%Y-%m-%d'))
            #     # (pd.to_datetime(DATASETS[config.time_col]) <= (datetime.strptime(config.row_end.strip(), '%Y-%m-%d') + timedelta(days=1)))
            # ]
            # DATASETS.interpolate(inplace=True)

            # datelist = np.array(DATASETS[config.time_col])
            # # datelist = np.array([datetime.strptime(date, '%Y-%m-%d').date() for date in list(DATASETS[config.time_col])])
            # featureset = DATASETS[config.feature]
            # vector_featureset = featureset.values

            # config.logs.append(f'Dataset Shape : {featureset.shape}\nFeatured Selected: : {config.feature}\nPredict Selected: : {config.feature}\n')
            # self.send(text_data=json.dumps({
            #     'message': config.logs[-1]
            # }))

            # scaller = MinMaxScaler()
            # vector_featureset_scaled = scaller.fit_transform(vector_featureset)

            # train_size = int(vector_featureset_scaled.size * 0.9)
            # trainset, testset = vector_featureset_scaled[0:train_size], vector_featureset_scaled[train_size:vector_featureset_scaled.size]
            # traindateset, testdateset = datelist[0:train_size], datelist[train_size:datelist.size]

            # X_train, y_train = train_test_split(trainset, time_step=config.timestep)
            # X_train = np.reshape(X_train, (X_train.shape[0], len(config.feature), X_train.shape[1]))
            
            # X_test, y_test = train_test_split(testset, time_step=config.timestep)
            # X_test = np.reshape(X_test, (X_test.shape[0], len(config.feature), X_test.shape[1]))
            
            # config.logs.append(f'Input (X) Train Shape : {X_train.shape}\nLabel (Y) Train Shape : {y_train.shape}\n\n')
            # self.send(text_data=json.dumps({
            #     'message': config.logs[-1]
            # }))
            
            # model = tf.keras.models.Sequential()

            # for i in range(0, config.layer_size):
            #     model.add(
            #         tf.keras.layers.LSTM(
            #             units=config.unit_size,
            #             return_sequences=False if i == config.layer_size - 1 else True,
            #             batch_input_shape=(config.max_batch_size, len(config.feature), config.timestep),
            #             go_backwards=True,
            #             dropout=config.dropout,
            #             # weights=[
            #             #     np.array([
            #             #         [0.5774, 0.5774, 0.5774, 0.5774],
            #             #         [0.5774, 0.5774, 0.5774, 0.5774]
            #             #     ]),
            #             #     np.array([
            #             #         [0.5774, 0.5774, 0.5774, 0.5774]
            #             #     ]),
            #             #     np.zeros([4])
            #             # ]
            #         )
            #     )
            # else:
            #     model.compile(
            #         optimizer=tf.keras.optimizers.SGD(learning_rate=config.learning_rate),
            #         loss=mean_squared_error,
            #         run_eagerly=True
            #     )
                
            #     def model_summary_callback(msg):
            #         config.logs.append(f'{msg}\n')
            #         self.send(text_data=json.dumps({
            #             'message': config.logs[-1] 
            #         }))
                
            #     model.summary(print_fn=model_summary_callback)

            # model.fit(X_train, y_train,
            #     shuffle=False,
            #     epochs=config.max_epoch,
            #     verbose=0,
            #     batch_size=config.max_batch_size,
            #     callbacks=[
            #         CustomCallback(
            #             websocket=self,
            #             X_train=X_train,
            #             X_test=X_test,
            #             config=config
            #         )
            #     ]
            # )
            
            # config.logs.append(f'Start Predicting\n')
            # self.send(text_data=json.dumps({
            #     'message': config.logs[-1]
            # }))
            
            # testset_split = proyeksi_split(testset, time_step=config.timestep)
            # testset_split_reshape = np.reshape(testset_split, (testset_split.shape[0], len(config.feature), testset_split.shape[1]))
            # proyeksi = model.predict(testset_split_reshape, verbose=0)
            # for i in range(0, proyeksi.size):
            #     testset[i + config.timestep - 1] = proyeksi[i]

            # for i in range(0, config.num_predict):
            #     config.logs.append(
            #         progress_bar(
            #             i + 1,
            #             config.num_predict,
            #             prefix=
            #             f'Predicting Days {str(i + 1)}/{str(config.num_predict)}',
            #             suffix=f'Completed',
            #             length=25
            #         )
            #     )
            #     self.send(text_data=json.dumps({
            #         'message': config.logs[-1] 
            #     }))
            #     testset_split = proyeksi_split(testset, time_step=config.timestep)
            #     testset_split_reshape = np.reshape(testset_split, (testset_split.shape[0], len(config.feature), testset_split.shape[1]))
            #     proyeksi = model.predict(testset_split_reshape, verbose=0)
            #     testset = np.concatenate((testset, np.array([proyeksi[-1]])), axis=0)
                
            # config.logs.append(f'\nPlotting Datasets...\n')
            # self.send(text_data=json.dumps({
            #     'message': config.logs[-1]
            # }))
            
            # testset = scaller.inverse_transform(testset)
            # testdateset = np.concatenate((testdateset, pd.to_datetime(pd.date_range(datelist[-1] + timedelta(days=1), periods=config.num_predict, freq='1d')).date), axis=0)
            
            # LABEL = np.concatenate((traindateset, testdateset), axis=0)
            
            # PREDICTIONS = pd.DataFrame(testset, columns=[config.feature]).set_index(pd.Series(testdateset))
            # PREDICTIONS.index = PREDICTIONS.index.to_series().apply(lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            
            # HISTORY = pd.DataFrame(np.array(DATASETS[config.feature]), columns=[config.feature]).set_index(pd.Series(datelist))
            # HISTORY.index = HISTORY.index.to_series().apply(lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))
            
            # START_DATE_FOR_PLOTTING = (datelist[-1] - timedelta(days=max((config.num_predict) * 3, 90))).strftime("%Y-%m-%d")
            # blank_index = (datelist[-(DATASETS.shape[0] - train_size + config.timestep - 1)]).strftime("%Y-%m-%d")

            # self.send(text_data=json.dumps({
            #     'results': {
            #         'prediction':
            #         pd.DataFrame({
            #             "tanggal": [
            #                 x.strftime('%d-%m-%Y')
            #                 for x in PREDICTIONS.loc[START_DATE_FOR_PLOTTING:].index
            #             ],
            #             config.feature[0]: [
            #                 x[0] for x in PREDICTIONS.loc[START_DATE_FOR_PLOTTING:][config.feature].values.tolist()
            #             ]
            #         }).to_dict('records'),
            #         'history':
            #         pd.DataFrame({
            #             "tanggal": [
            #                 x.strftime('%d-%m-%Y')
            #                 for x in HISTORY.loc[START_DATE_FOR_PLOTTING:].index
            #             ],
            #             config.feature[0]: [
            #                 x[0] for x in HISTORY.loc[START_DATE_FOR_PLOTTING:][config.feature].values.tolist()
            #             ]
            #         }).to_dict('records'),
            #     },
            #     "labels": [x.strftime('%d-%m-%Y') for x in LABEL.tolist()],
            #     "null": [
            #         0 for x in HISTORY.loc[START_DATE_FOR_PLOTTING:blank_index].index
            #     ]
            # }))
            
            # config.logs.append(f'\nHyperparameter tersimpan dalam Database...\n')
            # self.send(text_data=json.dumps({
            #     'message': config.logs[-1]
            # }))
            
            # Riwayat.objects.create(
            #     timestep = config.timestep,
            #     max_batch_size = config.max_batch_size,
            #     max_epoch = config.max_epoch,
            #     layer_size = config.layer_size,
            #     unit_size = config.unit_size,
            #     dropout = config.dropout,
            #     learning_rate = config.learning_rate,
            #     row_start = config.row_start,
            #     row_end = config.row_end,
            #     num_predict = config.num_predict,
            #     logs = config.timestep,
            #     hdf = config.timestep
            # )

            self.close()
        except Exception as e:
            self.send(text_data=json.dumps({
                'message': f'\n\nError : {e}\n'
            }))
            self.close()
