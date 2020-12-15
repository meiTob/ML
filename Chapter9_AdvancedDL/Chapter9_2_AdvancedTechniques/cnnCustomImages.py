import os
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import ELU
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import ReLU
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tf_utils.callbacks import LRTensorBoard
from tf_utils.callbacks import schedule_fn
from tf_utils.callbacks import schedule_fn2
from tf_utils.callbacks import schedule_fn3
from tf_utils.callbacks import schedule_fn4
from tf_utils.dogsCatsDataAdvanced import DOGSCATS


np.random.seed(0)
tf.random.set_seed(0)


CUSTOM_IMAGES_DIR = os.path.abspath("C:/Users/Jan/Documents/DogsAndCats/custom")
MODELS_DIR = os.path.abspath("C:/Users/Jan/Dropbox/_Programmieren/UdemyTF/models/")
if not os.path.exists(MODELS_DIR):
    os.mkdir(MODELS_DIR)
MODEL_FILE_PATH = os.path.join(MODELS_DIR, "dogs_cats.h5")
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
    dropout_rate: float,
    use_batch_normalization: bool,
    use_dense: bool,
    use_global_pooling: bool
) -> Model:
    input_img = Input(shape=img_shape)

    x = Conv2D(
        filters=filter_block1,
        kernel_size=kernel_size_block1,
        padding="same",
        kernel_initializer=kernel_initializer
    )(input_img)
    if use_batch_normalization:
        x = BatchNormalization()(x)
    x = activation_cls(x)
    x = Conv2D(
        filters=filter_block1,
        kernel_size=kernel_size_block1,
        padding="same", kernel_initializer=kernel_initializer
    )(x)
    if use_batch_normalization:
        x = BatchNormalization()(x)
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
    if use_batch_normalization:
        x = BatchNormalization()(x)
    x = activation_cls(x)
    x = Conv2D(
        filters=filter_block2,
        kernel_size=kernel_size_block2,
        padding="same",
        kernel_initializer=kernel_initializer
    )(x)
    if use_batch_normalization:
        x = BatchNormalization()(x)
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
    if use_batch_normalization:
        x = BatchNormalization()(x)
    x = activation_cls(x)
    x = Conv2D(
        filters=filter_block3,
        kernel_size=kernel_size_block3,
        padding="same",
        kernel_initializer=kernel_initializer
    )(x)
    if use_batch_normalization:
        x = BatchNormalization()(x)
    if dropout_rate:
        x = Dropout(rate=dropout_rate)(x)
    x = activation_cls(x)
    x = MaxPool2D()(x)

    if use_global_pooling:
        x = GlobalAveragePooling2D()(x)
    else:
        x = Flatten()(x)
    if use_dense:
        x = Dense(
            units=dense_layer_size,
            kernel_initializer=kernel_initializer
        )(x)
        if use_batch_normalization:
            x = BatchNormalization()(x)
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
    epochs = 100
    batch_size = 128

    params = {
        "dense_layer_size": 128,
        "kernel_initializer": "GlorotUniform",
        "optimizer": Adam,
        "learning_rate": 1e-3,
        "filter_block1": 32,
        "kernel_size_block1": 3,
        "filter_block2": 64,
        "kernel_size_block2": 3,
        "filter_block3": 128,
        "kernel_size_block3": 3,
        "activation_cls": ReLU(),
        "dropout_rate": 0.0,
        "use_batch_normalization": True,
        "use_dense": True,
        "use_global_pooling": True
    }

    model = build_model(
        img_shape,
        num_classes,
        **params
    )

    model_log_dir = os.path.join(LOGS_DIR, "modelFinal")

    lrs_callback = LearningRateScheduler(
        schedule=schedule_fn2,
        verbose=1
    )

    plateau_callback = ReduceLROnPlateau(
        monitor="val_accuracy",
        factor=0.99,
        patience=3,
        verbose=1,
        min_lr=1e-5
    )

    lr_callback = LRTensorBoard(
        log_dir=model_log_dir,
        histogram_freq=0,
        profile_batch=0,
        write_graph=False
    )

    es_callback = EarlyStopping(
        monitor="val_accuracy",
        patience=30,
        verbose=1,
        restore_best_weights=True,
        min_delta=0.0005
    )

    # model.fit(
    #     train_dataset,
    #     verbose=1,
    #     batch_size=batch_size,
    #     epochs=epochs,
    #     callbacks=[es_callback, lrs_callback, lr_callback],
    #     validation_data=val_dataset,
    # )

    # model.save_weights(MODEL_FILE_PATH)
    model.load_weights(MODEL_FILE_PATH)

    image_names = [f for f in os.listdir(CUSTOM_IMAGES_DIR) if ".jpg" in f or ".jpeg" in f or ".png" in f]
    class_names = ["cat", "dog"]

    for image_file_name in image_names:
        image_file_path = os.path.join(CUSTOM_IMAGES_DIR, image_file_name)
        x = data.load_and_preprocess_custom_image(image_file_path)
        x = np.expand_dims(x, axis=0)
        y_pred = model.predict(x)[0]
        y_pred_class_idx = np.argmax(y_pred)
        y_pred_prob = y_pred[y_pred_class_idx]
        y_pred_class_name = class_names[y_pred_class_idx]
        plt.imshow(x.reshape(64, 64, 3))
        plt.title(f"Pred class: {y_pred_class_name}, Prob: {y_pred_prob}")
        plt.show()
