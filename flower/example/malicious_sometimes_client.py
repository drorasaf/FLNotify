import random
import flwr as fl
import tensorflow as tf

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])




class CifarClient(fl.client.NumPyClient):
    perform_attack = 1
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        self.perform_attack = random.random() < 0.1
        scaled_x = self.scaling_attack(x_train, parameters)
        model.fit(scaled_x, y_train, epochs=1, batch_size=32, steps_per_epoch=3)
        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        scaled_x = self.scaling_attack(x_test, parameters)
        loss, accuracy = model.evaluate(scaled_x, y_test)
        return loss, len(scaled_x), {"accuracy": float(accuracy)}

    def scaling_attack(self, x, weights):
        if not self.perform_attack:
            return x
        scaling_factor = len(weights)
        scaled_x = x * scaling_factor
        return scaled_x

fl.client.start_numpy_client(server_address="[::]:8080", client=CifarClient())
