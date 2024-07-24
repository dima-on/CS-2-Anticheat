from pynput import mouse
import numpy as np
import json
import enum

class DataType(enum.Enum):
    Normal = 0
    Cheat = 1

class Data():
    def __init__(self, type_data, type_work):
        self.mouse_pos_delta = []
        self.all_data = []
        self.type_data = type_data

        if type_work == 0:
            self.mouse_control = mouse.Listener(on_move=self.get_mouse_position, on_click=self.get_click)
            self.mouse_control.start()
            self.mouse_control.join()
    def get_mouse_position(self, x_pos, y_pos):
        if len(self.mouse_pos_delta) > 0:
            x = self.mouse_pos_delta[len(self.mouse_pos_delta) - 1][0]
            y = self.mouse_pos_delta[len(self.mouse_pos_delta) - 1][1]
            x_delta = self.module(x - x_pos)
            y_delta = self.module(y - y_pos)
            mouse_speed = x_delta + y_delta

        else:
            mouse_speed = 0

        self.mouse_pos_delta.append([x_pos, y_pos, mouse_speed])

    def mean_speed(self, speed_arr):
        all_sum = 0
        speed_arr = speed_arr.tolist()
        for i in range(len(speed_arr)):
            all_sum += speed_arr[i]
        return all_sum / len(speed_arr)

    def only_speed(self, all_arr):
        all_arr = np.array(all_arr)
        speed_arr = all_arr[:, 2]
        return self.mean_speed(speed_arr)

    def get_click(self, x, y, button, pressed):
        if pressed and button == button.left:
            click_data = []
            print(self.mouse_pos_delta)
            if len(self.mouse_pos_delta) >= 10:
                for i in range(len(self.mouse_pos_delta) - 10, len(self.mouse_pos_delta)):
                    click_data.append(self.mouse_pos_delta[i])
            else:
                for i in range(len(self.mouse_pos_delta)):
                    click_data.append(self.mouse_pos_delta[i])


            if len(self.mouse_pos_delta) > 12:
                self.mouse_pos_delta = self.mouse_pos_delta[-1:]

            last_x = click_data[len(click_data) - 1][0]
            last_y = click_data[len(click_data) - 1][1]

            delta_x = self.module(last_x - x)
            delta_y = self.module(last_y - y)

            offset_click = delta_x + delta_y
            is_line = self.is_line(click_data)
            mean_speed = self.only_speed(click_data)

            out_data = [[mean_speed], [offset_click], [is_line]]

            compile_data = self.compile_data(out_data)

            self.all_data.append(compile_data)

            if len(self.all_data) > 10:
                print("all data")
                self.all_data = self.compile_data(self.all_data)
                self.save_data(self.all_data)
                self.all_data = []

    def is_line(self, points):
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        # Найдем коэффициенты линии наименьших квадратов
        line_kof = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(line_kof, y, rcond=None)[0]

        # Вычислим расстояния от точек до линии
        distances = np.abs(m * x + c - y) / np.sqrt(m ** 2 + 1)

        # Среднеквадратичное отклонение
        is_line = np.sqrt(np.mean(distances ** 2))

        return is_line

    def compile_data(self, click_data):
        compile_data = []
        print("ss")
        for i in range(len(click_data)):
            for k in range(len(click_data[i])):
                compile_data.append(click_data[i][k])
        return compile_data

    def module(self, x):
        if x < 0:
            return -x
        else:
            return x

    def save_data(self, compile_data):
        if self.type_data == DataType.Normal.value:
            name_json = "Normal.json"
        else:
            name_json = "Cheat.json"

        load_data = self.load_data()
        load_data.append(compile_data)
        with open(name_json, "w") as file:
            json.dump(load_data, file)


    def load_data(self):
        print(DataType.Normal.value)
        if self.type_data == DataType.Normal.value:
            name_json = "Normal.json"
        else:
            name_json = "Cheat.json"

        with open(name_json, "r") as file:
            data = json.load(file)
        return data

#My_Data = Data(1, 0)

