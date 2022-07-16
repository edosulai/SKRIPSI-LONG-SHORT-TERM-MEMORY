from tkinter import E
from channels.generic.websocket import WebsocketConsumer

from proyeksi.models import Klimatologi, Riwayat

import uuid
import json
import math
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

from proyeksi.utils import set_config, mean_absolute_error, mean_squared_error, root_mean_squared_error, train_test_split, proyeksi_split, progress_bar

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
                "feature": text_data_json['feature_training'].split(','),
                "prediction": text_data_json['feature_predict'],
                "model_name": str(uuid.uuid4().hex),
                "valueset": {
                    "results":{},
                    "loss_trains": [],
                    "loss_tests": [],
                    "labels":[],
                    "historylabels": [],
                    "logs": [],
                    "eva_error": 0
                },
            })
            
            if "id_riwayat" not in text_data_json:

                DATASETS = pd.DataFrame(list(klimatologi_data.values())).replace(to_replace=[8888, 9999, 2555], value=np.nan)
                DATASETS.interpolate(inplace=True)

                for feature in DATASETS:
                    if DATASETS[feature].dtypes == object and feature != config.time_col:
                        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=1)
                        tokenizer.fit_on_texts(DATASETS[feature].astype(str))
                        index_word = list(tokenizer.index_word.values())
                        
                        for index in index_word:
                            DATASETS = DATASETS.replace(to_replace=str(index.upper()), value=tokenizer.word_index[index], regex=True)
                    
                DATASETS = DATASETS.loc[
                    (pd.to_datetime(DATASETS[config.time_col]) >= datetime.strptime(config.row_start.strip(), '%Y-%m-%d')) & 
                    (pd.to_datetime(DATASETS[config.time_col]) <= datetime.strptime(config.row_end.strip(), '%Y-%m-%d'))
                ]
                
                DATELIST = np.array(DATASETS[config.time_col])
                # DATELIST = np.array([datetime.strptime(date, '%Y-%m-%d').date() for date in list(DATASETS[config.time_col])])
                
                featuresets = DATASETS[config.feature]

                config.valueset['logs'].append(f'Dataset Shape : {featuresets.shape}\nFeature Training : {config.feature}\nFeature Prediction : {config.prediction}\n')
                self.send(text_data=json.dumps({
                    'message': config.valueset['logs'][-1]
                }))

                featurescaller = MinMaxScaler()
                featuresets_scaled = featurescaller.fit_transform(featuresets)
                
                predictscaller = MinMaxScaler()
                predictscaller.fit_transform(featuresets[[config.prediction]])

                train_size = int(featuresets_scaled.shape[0] * 0.9)
                trainset, testset = featuresets_scaled[0:train_size], featuresets_scaled[train_size:featuresets_scaled.shape[0]]
                traindateset, testdateset = DATELIST[0:train_size], DATELIST[train_size:DATELIST.size]

                X_train, y_train = train_test_split(trainset, timestep=config.timestep)
                X_train = np.reshape(X_train, (X_train.shape[0], len(config.feature), X_train.shape[1]))
                y_train = np.reshape(y_train, (y_train.shape[0], len(config.feature), y_train.shape[1]))

                X_test, y_test = train_test_split(testset, timestep=config.timestep)
                X_test = np.reshape(X_test, (X_test.shape[0], len(config.feature), X_test.shape[1]))
                y_test = np.reshape(y_test, (y_test.shape[0], len(config.feature), y_test.shape[1]))
                
                config.valueset['logs'].append(f'Input (X) Train Shape : {X_train.shape}\nLabel (Y) Train Shape : {y_train.shape}\n\n')
                self.send(text_data=json.dumps({
                    'message': config.valueset['logs'][-1]
                }))
                
                model = tf.keras.models.Sequential()

                for i in range(0, config.layer_size):
                    model.add(tf.keras.layers.LSTM(
                        units=config.unit_size,
                        return_sequences=True,
                        batch_input_shape=(config.max_batch_size, len(config.feature), config.timestep),
                        go_backwards=True,
                        dropout=config.dropout,
                        weights=[
                            np.repeat([[0.5774, 0.5774, 0.5774, 0.5774]], repeats=config.timestep, axis=0),
                            np.repeat([[0.5774, 0.5774, 0.5774, 0.5774]], repeats=len(config.feature), axis=0),
                            np.zeros([4])
                        ]
                    ))
                else:
                    if config.unit_size > 1 :
                        model.add(tf.keras.layers.Dense(units=1, activation='linear'))
                    model.compile(
                        optimizer=tf.keras.optimizers.SGD(learning_rate=config.learning_rate),
                        # loss=mean_absolute_error,
                        loss=mean_squared_error,
                        # loss=root_mean_squared_error,
                        run_eagerly=True
                    )
                    
                    def model_summary_callback(msg):
                        config.valueset['logs'].append(f'{msg}\n')
                        self.send(text_data=json.dumps({
                            'message': config.valueset['logs'][-1] 
                        }))
                    
                    model.summary(print_fn=model_summary_callback)
                    

                def on_train_begin(logs=None):
                    config.valueset['logs'].append(f'\nStarting Training with Tensor 3D (Batch Size, Feature, Timestep Length) : ({X_train.shape[0]} , {len(config.feature)} , {config.timestep})\n')
                    self.send(text_data=json.dumps({
                        'message': config.valueset['logs'][-1]
                    }))   

                def on_train_end(logs=None):
                    # logs["loss"] = predictscaller.inverse_transform(np.reshape(logs["loss"], (1, 1)))[0][0]
                    
                    config.valueset['logs'].append(f'\nStop Training - loss: {round(logs["loss"], 5)}\n\n')
                    self.send(text_data=json.dumps({
                        'message': config.valueset['logs'][-1]
                    }))

                def on_epoch_begin(epoch, logs=None):
                    config.valueset['logs'].append(f'\nStart Epoch {epoch + 1}/{config.max_epoch}\n')
                    self.send(text_data=json.dumps({
                        'message': config.valueset['logs'][-1]
                    }))

                def on_epoch_end(epoch, logs=None):
                    # logs["loss"] = predictscaller.inverse_transform(np.reshape(logs["loss"], (1, 1)))[0][0]
                    
                    config.valueset['loss_trains'].append(logs["loss"])
                    config.valueset['logs'].append(f'End Epoch {epoch + 1}/{config.max_epoch} of training - loss: {round(logs["loss"], 5)}\n')
                    self.send(text_data=json.dumps({
                        'message': config.valueset['logs'][-1]
                    }))

                def on_batch_end(batch, logs=None):
                    # logs["loss"] = predictscaller.inverse_transform(np.reshape(logs["loss"], (1, 1)))[0][0]
                    
                    if batch == X_train.shape[0] - 1:
                        config.valueset['logs'].append(progress_bar(
                                batch + 1,
                                X_train.shape[0],
                                prefix=f'Training Batch {str(batch + 1)}/{str(X_train.shape[0])}',
                                suffix=f'Completed - loss: {str(round(logs["loss"], 5))}',
                                length=25
                            ))
                        self.send(text_data=json.dumps({
                            'message': config.valueset['logs'][-1]
                        }))
                    else:
                        self.send(text_data=json.dumps({
                            'message': progress_bar(
                                batch + 1,
                                X_train.shape[0],
                                prefix=f'Training Batch {str(batch + 1)}/{str(X_train.shape[0])}',
                                suffix=f'Completed - loss: {str(round(logs["loss"], 5))}',
                                length=25
                            )
                        }))

                model.fit(X_train, y_train,
                    shuffle=False,
                    epochs=config.max_epoch,
                    verbose=0,
                    batch_size=config.max_batch_size,
                    callbacks=[
                        tf.keras.callbacks.LambdaCallback(
                            on_epoch_begin=on_epoch_begin,
                            on_epoch_end=on_epoch_end,
                            on_batch_begin=None,
                            on_batch_end=on_batch_end,
                            on_train_begin=on_train_begin,
                            on_train_end=on_train_end,
                        )
                    ]
                )
                class CustomCallback(tf.keras.callbacks.Callback):
                    def on_test_batch_end(self, batch, logs=None):
                        config.valueset['loss_tests'].append(logs["loss"])
                        # config.valueset['loss_tests'].append(predictscaller.inverse_transform(np.reshape(logs["loss"], (1, 1)))[0][0])
                        # config.valueset['loss_tests'].append(predictscaller.inverse_transform(np.reshape(math.sqrt(logs["loss"]), (1, 1)))[0][0])
                
                config.valueset['eva_error'] = model.evaluate(
                    X_test,
                    y_test,
                    verbose=0,
                    batch_size=config.max_batch_size,
                    callbacks=[CustomCallback()]
                )
                # config.valueset['eva_error'] = predictscaller.inverse_transform(np.reshape(config.valueset['eva_error'], (1, 1)))[0][0]
                # config.valueset['eva_error'] = predictscaller.inverse_transform(np.reshape(math.sqrt(config.valueset['eva_error']), (1, 1)))[0][0]
                
                config.valueset['logs'].append(f'Start Predicting\n')
                self.send(text_data=json.dumps({
                    'message': config.valueset['logs'][-1]
                }))
                
                testset_split = proyeksi_split(testset, timestep=config.timestep)
                testset_split_reshape = np.reshape(testset_split, (testset_split.shape[0], len(config.feature), testset_split.shape[1]))
                proyeksi = model.predict(testset_split_reshape, verbose=0, batch_size=1)
                for i in range(0, proyeksi.shape[0]):
                    testset[i + config.timestep - 1] = np.reshape(proyeksi[i], (proyeksi[i].shape[1], len(config.feature)))
                    
                for i in range(0, config.num_predict):
                    config.valueset['logs'].append(progress_bar(
                        i + 1,
                        config.num_predict,
                        prefix=f'Predicting Days {str(i + 1)}/{str(config.num_predict)}',
                        suffix=f'Completed',
                        length=25
                    ))
                    self.send(text_data=json.dumps({
                        'message': config.valueset['logs'][-1] 
                    }))
                    testset_split = proyeksi_split(testset, timestep=config.timestep)
                    testset_split_reshape = np.reshape(testset_split, (testset_split.shape[0], len(config.feature), testset_split.shape[1]))
                    proyeksi = model.predict(testset_split_reshape, verbose=0, batch_size=1)
                    testset = np.concatenate((testset, np.reshape(proyeksi[-1], (proyeksi[-1].shape[1], len(config.feature)))), axis=0)
                    
                
                config.valueset['logs'].append(f'\nPlotting Datasets...\n')
                self.send(text_data=json.dumps({
                    'message': config.valueset['logs'][-1]
                }))
                
                testset = featurescaller.inverse_transform(testset)
                testdateset = np.concatenate((testdateset, pd.to_datetime(pd.date_range(DATELIST[-1] + timedelta(days=1), periods=config.num_predict, freq='1d')).date), axis=0)

                LABEL = np.concatenate((traindateset, testdateset), axis=0)

                PREDICTIONS = pd.DataFrame(testset, columns=[config.feature]).set_index(pd.Series(testdateset))
                PREDICTIONS.index = PREDICTIONS.index.to_series().apply(lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))

                # HISTORY = pd.DataFrame(np.array(featurescaller.fit_transform(DATASETS[config.feature])), columns=[config.feature]).set_index(pd.Series(DATELIST))
                HISTORY = pd.DataFrame(np.array(DATASETS[config.feature]), columns=[config.feature]).set_index(pd.Series(DATELIST))
                HISTORY.index = HISTORY.index.to_series().apply(lambda x: datetime.strptime(x.strftime('%Y-%m-%d'), '%Y-%m-%d'))

                START_DATE_FOR_PLOTTING = (DATELIST[-1] - timedelta(days=max((config.num_predict) * 3, 90))).strftime("%Y-%m-%d")
                blank_index = (DATELIST[-(DATASETS.shape[0] - train_size + config.timestep - 1)]).strftime("%Y-%m-%d")
                
                config.valueset['results'] = {
                    'prediction': {
                        "nama": config.prediction,
                        "hasil":pd.DataFrame({
                            "tanggal": [
                                x.strftime('%d/%m/%y')
                                for x in PREDICTIONS.loc[START_DATE_FOR_PLOTTING:].index
                            ],
                            "nilai": [
                                x[0] for x in PREDICTIONS.loc[START_DATE_FOR_PLOTTING:][config.prediction].values.tolist()
                            ]
                        }).to_dict('records')
                    },
                    'history': [
                        {
                            "nama": feature,
                            "hasil": pd.DataFrame({
                                "tanggal": [
                                    x.strftime('%d/%m/%y')
                                    for x in HISTORY.loc[START_DATE_FOR_PLOTTING:].index
                                ],
                                "nilai": [
                                    x[0] for x in HISTORY.loc[START_DATE_FOR_PLOTTING:][feature].values.tolist()
                                ]
                            }).to_dict('records')
                        } for feature in config.feature
                    ]
                }
                
                config.valueset['labels'] = [x.strftime('%d/%m/%y') for x in LABEL.tolist()]
                
                config.valueset['historylabels'] = [
                    x.strftime('%d/%m/%y') for x in HISTORY.loc[START_DATE_FOR_PLOTTING:blank_index].index
                ]
                
                config.valueset['logs'].append(f'\nHasil Proyeksi dan Nilai Hyperparameter tersimpan dalam Database...\n\n')
                self.send(text_data=json.dumps({
                    'message': config.valueset['logs'][-1]
                }))
                
                self.send(text_data=json.dumps(config.valueset))
                
                # model.save(f'media/{config.model_name}.h5')
                Riwayat.objects.create(
                    timestep = config.timestep,
                    max_batch_size = config.max_batch_size,
                    max_epoch = config.max_epoch,
                    layer_size = config.layer_size,
                    unit_size = config.unit_size,
                    dropout = config.dropout,
                    learning_rate = config.learning_rate,
                    row_start = config.row_start,
                    row_end = config.row_end,
                    num_predict = config.num_predict,
                    feature_training = text_data_json['feature_training'],
                    feature_predict = config.prediction,
                    loss = config.valueset['eva_error'],
                    valueset = json.dumps(config.valueset),
                    hdf = config.model_name
                )
                
            else:
                riwayat = Riwayat.objects.get(id=text_data_json['id_riwayat'])
                valueset = json.loads(riwayat.valueset)
                self.send(text_data=json.dumps(valueset))
                for log in valueset['logs']:
                    self.send(text_data=json.dumps({'message': log}))

            self.close()
        except Exception as e:  
            self.send(text_data=json.dumps({
                'message': f'\n\nError : {e}\n'
            }))
            self.close()
