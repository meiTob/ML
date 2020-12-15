import os
from typing import Tuple

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import ELU
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import ReLU
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tf_utils.dogsCatsDataAdvanced import DOGSCATS


np.random.seed(0)
tf.random.set_seed(0)


LOGS_DIR = os.path.abspath("C:/Users/Jan/Dropbox/_Programmieren/UdemyTF/logs/")
if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)


def build_model(
    img_shape: Tuple[int, int, int],
    num_classes: int,
    optimizer: tf.keras.optimizers.Optimizer,
    learning_rate: float,
    filter_block1: int,
    kernel_size_block1: int,
    filter_block2: int,
    kernel_size_block2: int,
    filter_block3: int,
    kernel_size_block3: int,
    dense_layer_size: int,
    kernel_initializer: tf.keras.initializers.Initializer,
    activation_cls: tf.keras.layers.Activation,
    dropout_rate: float
) -> Model:
    input_img = Input(shape=img_shape)

    x = Conv2D(
        filters=filter_block1,
        kernel_size=kernel_size_block1,
        padding="same",
        kernel_initializer=kernel_initializer
    )(input_img)
    x = activation_cls(x)
    x = Conv2D(
        filters=filter_block1,
        kernel_size=kernel_size_block1,
        padding="same", kernel_initializer=kernel_initializer
    )(x)
    if dropout_rate:
        x = Dropout(rate=dropout_rate)(x)
    x = activation_cls(x)
    x = MaxPool2D()(x)

    x = Conv2D(
        filters=filter_block2,
        kernel_size=kernel_size_block2,
        padding="same",
        kernel_initializer=kernel_initializer
    )(x)
    x = activation_cls(x)
    x = Conv2D(
        filters=filter_block2,
        kernel_size=kernel_size_block2,
        padding="same",
        kernel_initializer=kernel_initializer
    )(x)
    if dropout_rate:
        x = Dropout(rate=dropout_rate)(x)
    x = activation_cls(x)
    x = MaxPool2D()(x)

    x = Conv2D(
        filters=filter_block3,
        kernel_size=kernel_size_block3,
        padding="same",
        kernel_initializer=kernel_initializer
    )(x)
    x = activation_cls(x)
    x = Conv2D(
        filters=filter_block3,
        kernel_size=kernel_size_block3,
        padding="same",
        kernel_initializer=kernel_initializer
    )(x)
    if dropout_rate:
        x = Dropout(rate=dropout_rate)(x)
    x = activation_cls(x)
    x = MaxPool2D()(x)

    x = Flatten()(x)
    x = Dense(
        units=dense_layer_size,
        kernel_initializer=kernel_initializer
    )(x)
    x = activation_cls(x)
    x = Dense(
        units=num_classes,
        kernel_initializer=kernel_initializer
    )(x)
    y_pred = Activation("softmax")(x)

    model = Model(
        inputs=[input_img],
        outputs=[y_pred]
    )

    opt = optimizer(learning_rate=learning_rate)

    model.compile(
        loss="categorical_crossentropy",
        optimizer=opt,
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    data = DOGSCATS()

    train_dataset = data.get_train_set()
    val_dataset = data.get_val_set()
    test_dataset = data.get_test_set()

    img_shape = data.img_shape
    num_classes = data.num_classes

    # Global params
    epochs = 40
    batch_size = 128

    # Best model params
    optimizer = Adam
    learning_rate = 1e-3
    filter_block1 = 32
    kernel_size_block1 = 3
    filter_block2 = 64
    kernel_size_block2 = 3
    filter_block3 = 128
    kernel_size_block3 = 3
    dense_layer_size = 128
    kernel_initializer = "GlorotUniform"
    activation_cls = ReLU()

    dropout_rates = [0.0, 0.1, 0.2, 0.3]

    for dropout_rate in dropout_rates:
        dropout_name = f"DROPOUT_{dropout_rate}"

        model = build_model(
            img_shape,
            num_classes,
            optimizer,
            learning_rate,
            filter_block1,
            kernel_size_block1,
            filter_block2,
            kernel_size_block2,
            filter_block3,
            kernel_size_block3,
            dense_layer_size,
            kernel_initializer,
            activation_cls,
            dropout_rate
        )
        model_log_dir = os.path.join(LOGS_DIR, f"model{dropout_name}")

        tb_callback = TensorBoard(
            log_dir=model_log_dir,
            histogram_freq=0,
            profile_batch=0,
            write_graph=False
        )

        model.fit(
            train_dataset,
            verbose=1,
            batch_size=batch_size,
            epochs=epochs,
            callbacks=[tb_callback],
            validation_data=val_dataset,
        )
