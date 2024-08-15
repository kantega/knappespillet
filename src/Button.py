from Light import Light


class Button:
    def __init__(self):
        self.num_lights = 12
        self.lights = []
        for i in range(self.num_lights):
            self.lights.append(Light())

    def set_all_lights(self, light: Light):
        for i in range(self.num_lights):
            self.lights[i] = light
