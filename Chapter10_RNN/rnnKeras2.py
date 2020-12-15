import random

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.models import Sequential


np.random.seed(0)
tf.random.set_seed(0)


def sigmoid_fn(x: np.ndarray) -> np.ndarray:
    return x  # TODO


def tanh_fn(x: np.ndarray) -> np.ndarray:
    return x  # TODO


class SimpleRNNInference:
    def __init__(
        self,
        rnn_layer: tf.keras.layers.SimpleRNN,
        return_sequences: bool = False
    ) -> None:
        self.return_sequences = return_sequences
        self.rnn_layer = rnn_layer
        self.W, self.U, self.b = self.rnn_layer.get_weights()
        self.units = self.b.shape[0]

    def __call__(
        self,
        x: np.ndarray
    ) -> None:
        print(self.W)
        print(self.U)
        print(self.b)

    def forward_step(self) -> None:
        pass


if __name__ == "__main__":
    # data set shape = (num_samples, num_timesteps, num_features)
    # input shape = (num_timesteps, num_features)
    # If return_sequences == True:
    # output shape = (num_timesteps, units)
    # Else:
    # output shape = (1, units)
    x = np.random.normal(size=(1, 3, 2))
    units = 4
    return_sequences = False

    # num_features = 2
    # units = 4
    # h_t shape = (4),        (units)
    # W shape   = (2, 4),     (num_features, units)
    # U shape   = (4, 4),     (units, units)
    # b shape   = (4),        (units)
    #
    # matmul(x, W)      (2)*(2,4) => (4)
    # matmul(h, U)      (4)*(4,4) => (4)
    # intern + b        (4)+(4)   => (4)
    model = Sequential()
    model.add(SimpleRNN(units=units, return_sequences=return_sequences, input_shape=x.shape[1:]))
    model.compile(loss="mse", optimizer="Adam")
    # model.summary()

    rnn = SimpleRNNInference(rnn_layer=model.layers[0], return_sequences=return_sequences)
    output_rnn_own = rnn(x[0])  # 10.5
    print(output_rnn_own)
    print("\n\n")
    output_rnn_tf = model.predict(x[[0]])
    print(output_rnn_tf)  # 10.5
    assert np.all(np.isclose(output_rnn_own - output_rnn_tf, 0.0))
