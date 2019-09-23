import torch
import pandas as pd
import numpy as np
from .tools import Tools
from threading import Thread
import json

class LNN:
    def __init__(self, seasonality):
        dtype = torch.float
        device = torch.device('cpu')
        self.seasonality = seasonality
        self.w1 = torch.randn(seasonality, 100, dtype=dtype, device=device, requires_grad=True)
        self.w2 = torch.randn(100, seasonality, dtype=dtype, device=device, requires_grad=True)
        self.learning_rate = 1e-4
       
    def forward(self, X):
        return torch.sigmoid(X.mm(self.w1)).mm(self.w2)

    def loss(self, actual, predict):
        return (actual - predict).pow(2).sum()

    def backpropagation(self, loss):
        loss.backward()
        with torch.no_grad():
            self.w1 -= self.learning_rate*self.w1.grad
            self.w2 -= self.learning_rate*self.w2.grad
            self.w1.grad.zero_()
            self.w2.grad.zero_()
    
    def percentage_error(self, Y, y):
        return ((y - Y)/Y).sum().item() *100

    def train(self, X, Y):
        for t in range(1000000):
            y = self.forward(X)

            lossing = self.loss(Y, y)

            self.backpropagation(lossing)

        return y
        #self.tmp.append({'w1': self.w1, 'w2': self.w2, 'y': y})

    def cross_validation(self, X, Y):
        best_error = float('inf')
        wheights = {}
        for i in range(5):
            y = self.train(X, Y)
            
            error = self.percentage_error(Y, y)

            if error < best_error:
                best_error = error
                wheights = {'w1': self.w1, 'w2': self.w2, 'error': error}

        self.w1 = wheights['w1']
        self.w2 = wheights['w2']

        return wheights['error']

    def predict(self, dataset, columns):
        helper = Tools()
        raw_dataset = helper.get_dataset(dataset, columns)
        dataset = helper.convert_to_log(raw_dataset, helper.seasonality_to_string(self.seasonality))
        tot_time = len(dataset)
        test_time = tot_time - self.seasonality
        x = dataset[columns[1]][:-self.seasonality]
        y = dataset[columns[1]][-test_time:]
        p = dataset[columns[1]][-self.seasonality:]
        start = dataset.index[-1:]
        X = torch.FloatTensor(helper.seasonality_generate(x, self.seasonality))
        Y = torch.FloatTensor(helper.seasonality_generate(y, self.seasonality))
        P = torch.FloatTensor(helper.seasonality_generate(p, self.seasonality))
        error = self.cross_validation(X, Y)
        prevision = torch.exp(self.forward(P)).tolist()[0]
        return helper.neural_json_parse(start, prevision, 'M')

    



