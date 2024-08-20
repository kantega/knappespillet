from typing import List
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

    def set_n_lights(self, n, light: Light):
        for i in range(n):
            self.lights[i] = light
        for i in range(n, self.num_lights):
            self.lights[i] = Light(0, 0, 0)

    def set_lights(self, lights: List[Light]):
        if len(lights) != self.num_lights:
            raise ValueError(f"Length of lights is not {self.num_lights}, was {len(lights)}")
        self.lights = lights
