from tensorflow.contrib.keras.python.keras.activations import relu
from tensorflow.contrib.keras.python.keras.engine.topology import Input
from tensorflow.contrib.keras.python.keras.engine.training import Model
from tensorflow.contrib.keras.python.keras.layers.advanced_activations import LeakyReLU
from tensorflow.contrib.keras.python.keras.layers.core import Dense, Dropout
from tensorflow.contrib.keras.python.keras.optimizers import Adam, RMSprop


class Model1:

    def __init__(self):
        self.model = self.build()

    def build(self):
        d_input = Input(shape=(2, ))

        x = Dense(64, activation='relu')(d_input)
        x = Dropout(0.5)(x)

        x = Dense(64, activation='relu')(x)
        x = Dropout(0.5)(x)

        x = Dense(64, activation='relu')(x)
        x = Dropout(0.5)(x)

        x = Dense(64, activation='relu')(x)
        x = Dropout(0.5)(x)

        d_output = Dense(3, activation="relu")(x)

        model = Model(inputs=[d_input], outputs=[d_output])
        optimizer = Adam(lr=0.00005)
        model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

        return model

