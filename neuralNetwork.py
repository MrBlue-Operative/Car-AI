import numpy as np
import pygame as py
from config import screen
import random as rn

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

class level:
    def __init__(self, inputCount, outputCount):
        self.inputs = inputCount
        self.outputs = outputCount
        self.weights = []
        self.bias = np.random.uniform(low=-1, high=1, size=self.outputs)
        for i in range(outputCount):
            numbers = np.random.uniform(low=-1, high=1, size=self.inputs)
            self.weights.append(numbers)
        
        self.i_values = np.zeros(inputCount)
        self.o_values = np.zeros(outputCount)

        
    def compute(self, inputValues):
        self.i_values = inputValues
        for i in range(self.outputs):
            sum = 0
            for j in range(self.inputs):
                sum += self.i_values[j]*self.weights[i][j]
            sum += self.bias[i]
            self.o_values[i] = sigmoid(sum)

# This is a 3 level Neural Network
class NeuralNetwork:
    def __init__(self, neurons):
        self.lvl1 = level(neurons[0], neurons[1])
        self.lvl2 = level(neurons[1], neurons[2])
        self.neurons = neurons
        self.binary_output = 0
        self.inputs = None

    def fit(self, inputs):
        self.inputs = inputs
        self.lvl1.compute(inputs)
        self.lvl2.compute(self.lvl1.o_values)
        self.binary_output = np.where(self.lvl2.o_values > 0.5, 1, 0)
        return self.binary_output
    
    def mutate(self, base_network, mutation_rate=0.1):
        
        if (self.lvl1.inputs != base_network.lvl1.inputs or
            self.lvl1.outputs != base_network.lvl1.outputs or
            self.lvl2.inputs != base_network.lvl2.inputs or
            self.lvl2.outputs != base_network.lvl2.outputs):
            raise ValueError("Base network must have the same architecture")

        for i in range(self.lvl1.outputs):

            self.lvl1.weights[i] = base_network.lvl1.weights[i].copy() + np.random.normal(0, mutation_rate, size=self.lvl1.inputs)
            self.lvl1.weights[i] = np.clip(self.lvl1.weights[i], -1, 1)  
        self.lvl1.bias = base_network.lvl1.bias.copy() + np.random.normal(0, mutation_rate, size=self.lvl1.outputs)
        self.lvl1.bias = np.clip(self.lvl1.bias, -1, 1) 
        
        for i in range(self.lvl2.outputs):
            
            self.lvl2.weights[i] = base_network.lvl2.weights[i].copy() + np.random.normal(0, mutation_rate, size=self.lvl2.inputs)
            self.lvl2.weights[i] = np.clip(self.lvl2.weights[i], -1, 1)  
        self.lvl2.bias = base_network.lvl2.bias.copy() + np.random.normal(0, mutation_rate, size=self.lvl2.outputs)
        self.lvl2.bias = np.clip(self.lvl2.bias, -1, 1)

    def visualizer(self, x, y):
        shift = 150

        def color(value):
            r = int(255 * value)
            g = int(255 * value)
            b = 0
            return (r, g, b)
        
        def printCircles(n, x, y, lvl, space=0, last=False):
            for i in range(n):
                py.draw.circle(screen, color(sigmoid(lvl[i]) if lvl[i] > 1 or lvl[i] < 0 else lvl[i]) if not last else color(self.binary_output[i]), (x, y + space), 15)
                py.draw.circle(screen, (0, 0, 0), (x, y + space), 15, 1)
                y += 70
        
        def printLines(n, m, x, y, space=0, spaceStart=0):
            for i in range(n):
                s = 70
                for j in range(m):
                    py.draw.line(screen, (0, 0, 0), (x, y + s*i + spaceStart), (x + shift, y + s*j + space), 2)
                
                    
        printLines(self.neurons[0], self.neurons[1], x, y, spaceStart=0)
        printLines(self.neurons[1], self.neurons[2], x + shift, y, space=0)

        printCircles(self.neurons[0], x, y, self.inputs, space=0)
        printCircles(self.neurons[1], x + shift, y, self.lvl1.o_values)
        printCircles(self.neurons[2], x + shift*2, y, self.lvl2.o_values, last=True, space=0)
    
    def save(self, filename):
        np.savez(filename,
                 lvl1_weights=self.lvl1.weights,
                 lvl1_bias=self.lvl1.bias,
                 lvl2_weights=self.lvl2.weights,
                 lvl2_bias=self.lvl2.bias)

    def load(self, filename):
        try:
            data = np.load(filename)
            self.lvl1.weights = data['lvl1_weights']
            self.lvl1.bias = data['lvl1_bias']
            self.lvl2.weights = data['lvl2_weights']
            self.lvl2.bias = data['lvl2_bias']
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find file: {filename}")
        except KeyError as e:
            raise KeyError(f"Missing expected array in .npz file: {e}")


class NeuralNetwork4:
    def __init__(self, neurons):
        if len(neurons) != 4:
            raise ValueError("Expected 4 values for neurons: [input, hidden1, hidden2, output]")
        self.lvl1 = level(neurons[0], neurons[1])
        self.lvl2 = level(neurons[1], neurons[2])
        self.lvl3 = level(neurons[2], neurons[3])  
        self.neurons = neurons
        self.binary_output = 0
        self.inputs = None

    def fit(self, inputs):
        self.inputs = inputs
        self.lvl1.compute(inputs)             
        self.lvl2.compute(self.lvl1.o_values)  
        self.lvl3.compute(self.lvl2.o_values)  
        self.binary_output = np.where(self.lvl3.o_values > 0.5, 1, 0)
        return self.binary_output

    def mutate(self, base_network, mutation_rate=0.1):
        
        if (self.lvl1.inputs != base_network.lvl1.inputs or
            self.lvl1.outputs != base_network.lvl1.outputs or
            self.lvl2.inputs != base_network.lvl2.inputs or
            self.lvl2.outputs != base_network.lvl2.outputs or
            self.lvl3.inputs != base_network.lvl3.inputs or
            self.lvl3.outputs != base_network.lvl3.outputs):
            raise ValueError("Base network must have the same architecture")

        for i in range(self.lvl1.outputs):
            self.lvl1.weights[i] = base_network.lvl1.weights[i].copy() + np.random.normal(0, mutation_rate, size=self.lvl1.inputs)
            self.lvl1.weights[i] = np.clip(self.lvl1.weights[i], -1, 1)
        self.lvl1.bias = base_network.lvl1.bias.copy() + np.random.normal(0, mutation_rate, size=self.lvl1.outputs)
        self.lvl1.bias = np.clip(self.lvl1.bias, -1, 1)

        for i in range(self.lvl2.outputs):
            self.lvl2.weights[i] = base_network.lvl2.weights[i].copy() + np.random.normal(0, mutation_rate, size=self.lvl2.inputs)
            self.lvl2.weights[i] = np.clip(self.lvl2.weights[i], -1, 1)
        self.lvl2.bias = base_network.lvl2.bias.copy() + np.random.normal(0, mutation_rate, size=self.lvl2.outputs)
        self.lvl2.bias = np.clip(self.lvl2.bias, -1, 1)

        for i in range(self.lvl3.outputs):
            self.lvl3.weights[i] = base_network.lvl3.weights[i].copy() + np.random.normal(0, mutation_rate, size=self.lvl3.inputs)
            self.lvl3.weights[i] = np.clip(self.lvl3.weights[i], -1, 1)
        self.lvl3.bias = base_network.lvl3.bias.copy() + np.random.normal(0, mutation_rate, size=self.lvl3.outputs)
        self.lvl3.bias = np.clip(self.lvl3.bias, -1, 1)

    def visualizer(self, x, y):
        shift = 100

        def color(value):
            r = int(255 * value)
            g = int(255 * value)
            b = 0
            return (r, g, b)

        def printCircles(n, x, y, lvl, space=0, last=False):
            for i in range(n):
                py.draw.circle(screen, color(sigmoid(lvl[i]) if lvl[i] > 1 or lvl[i] < 0 else lvl[i]) if not last else color(self.binary_output[i]), (x, y + space), 15)
                py.draw.circle(screen, (0, 0, 0), (x, y + space), 15, 1)
                y += 70

        def printLines(n, m, x, y, space=0, spaceStart=0):
            for i in range(n):
                s = 70
                for j in range(m):
                    py.draw.line(screen, (0, 0, 0), (x, y + s*i + spaceStart), (x + shift, y + s*j + space), 2)

        printLines(self.neurons[0], self.neurons[1], x, y, spaceStart=80, space=20)
        printLines(self.neurons[1], self.neurons[2], x + shift, y, space=60, spaceStart=20)
        printLines(self.neurons[2], self.neurons[3], x + 2*shift, y, space=130, spaceStart=60)

        printCircles(self.neurons[0], x, y, self.inputs, space=80)
        printCircles(self.neurons[1], x + shift, y, self.lvl1.o_values, space=20)
        printCircles(self.neurons[2], x + 2*shift, y, self.lvl2.o_values, space=60)
        printCircles(self.neurons[3], x + 3*shift, y, self.lvl3.o_values, last=True, space=130)

    def save(self, filename):
        np.savez(filename,
                 lvl1_weights=self.lvl1.weights,
                 lvl1_bias=self.lvl1.bias,
                 lvl2_weights=self.lvl2.weights,
                 lvl2_bias=self.lvl2.bias,
                 lvl3_weights=self.lvl3.weights,
                 lvl3_bias=self.lvl3.bias)

    def load(self, filename):
        try:
            data = np.load(filename)
            self.lvl1.weights = data['lvl1_weights']
            self.lvl1.bias = data['lvl1_bias']
            self.lvl2.weights = data['lvl2_weights']
            self.lvl2.bias = data['lvl2_bias']
            self.lvl3.weights = data['lvl3_weights']
            self.lvl3.bias = data['lvl3_bias']
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find file: {filename}")
        except KeyError as e:
            raise KeyError(f"Missing expected array in .npz file: {e}")