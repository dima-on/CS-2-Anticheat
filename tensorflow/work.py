import numpy as np
from keras.models import load_model
import Get_Data
import keras

model = load_model('model.h5', custom_objects={'mse': keras.losses.mean_squared_error})
Data = Get_Data.Data(0, 1)
N_data = Data.load_data()
Data_C = Get_Data.Data(1, 1)
C_data = Data_C.load_data()

count_correct = 0

for i in range(len(N_data)):
    N_data_new = np.array(N_data[i])
    input_data = N_data_new.reshape(1, -1)

    pred = model.predict(input_data)
    if pred[0] < 0.5:
        count_correct += 1


for i in range(len(C_data)):
    C_data_new = np.array(C_data[i])
    input_data = C_data_new.reshape(1, -1)

    pred = model.predict(input_data)
    if pred[0] > 0.5:
        count_correct += 1

accuracy = count_correct / (len(N_data) + len(C_data))
print(accuracy)