import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import Get_Data

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, hidden_size1,
                 hidden_size2,hidden_size3, hidden_size4,hidden_size5,
                 output_size, activation="relu"):
        self.model = Sequential([
            Dense(hidden_size, input_dim=input_size, activation=activation),
            Dense(hidden_size1, activation=activation),
            Dense(hidden_size2, activation=activation),
            Dense(hidden_size3, activation=activation),
            Dense(hidden_size4, activation=activation),
            Dense(hidden_size5, activation=activation),
            Dense(output_size, activation="sigmoid")
        ])
        self.model.compile(optimizer=Adam(learning_rate=0.01), loss='mse')

    def fit_network(self, X, y, epochs):
        self.model.fit(X, y, epochs=epochs)

    def predict(self, data):
        return self.model.predict(data)

    def save(self):
        self.model.save('model.h5')




def main():
    input_size = 33
    hidden_size = 64
    hidden_size1 = 32
    hidden_size2 = 16
    hidden_size3 = 8
    hidden_size4 = 4
    hidden_size5 = 2
    output_size = 1

    Normal_Data = Get_Data.Data(Get_Data.DataType.Normal.value, 1)
    Normal_Data_X = Normal_Data.load_data()
    Normal_Data_Y = []
    for i in range(len(Normal_Data.load_data())):
        Normal_Data_Y.append([0])

    Cheat_Data = Get_Data.Data(Get_Data.DataType.Cheat.value, 1)
    Cheat_Data_X = Cheat_Data.load_data()
    Cheat_Data_Y = []
    for i in range(len(Cheat_Data.load_data())):
        Cheat_Data_Y.append([1])

    for i in range(len(Cheat_Data.load_data())):
        Normal_Data_X.append(Cheat_Data_X[i])
        Normal_Data_Y.append(Cheat_Data_Y[i])

    X_normal = np.array(Normal_Data_X)
    y_normal = np.array(Normal_Data_Y)

    NN = NeuralNetwork(input_size, hidden_size, hidden_size1,
                       hidden_size2,hidden_size3,hidden_size4,
                       hidden_size5, output_size)

    NN.fit_network(X_normal, y_normal, epochs=200)
    NN.save()


if __name__ == "__main__":
    main()