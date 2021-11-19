
!pip install flask-ngrok

import torch
import torchvision
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math
import torch.optim as opt
import torch.nn.functional as F

#CUDA_VISIBLE_DEVICES=""

class RegressionTrainDataset(Dataset):

    def __init__(self):
        xy = np.loadtxt('regression_train.csv', delimiter=',', dtype=np.float32, skiprows=1)
        self.br_uzoraka = xy.shape[0]
      
        self.x_data = torch.from_numpy(xy[:, 1:]) 
        self.y_data = torch.from_numpy(xy[:, [0]])

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.br_uzoraka

train_set = RegressionTrainDataset()


train_loader = DataLoader(dataset=train_set,
                          batch_size=5,
                          shuffle=True,
                          num_workers=2)


class MyNeuralNetwork(torch.nn.Module):
    def __init__(self, input_size):
        super(MyNeuralNetwork, self).__init__()

        self.input_size = input_size

        self.linear_1 = torch.nn.Linear(input_size, 35)
        self.linear_2 = torch.nn.Linear(35, 35)
        self.linear_3 = torch.nn.Linear(35, 1)

    def forward(self, x):
        out = F.relu(self.linear_1(x))
        out = F.relu(self.linear_2(out))
        out = self.linear_3(out)
        return out

predictor=MyNeuralNetwork(5)

optimizer=opt.Adam(mreza.parameters(), lr=0.01)
f_loss=torch.nn.MSELoss()

num_epochs = 15

for epoch in range(num_epochs):
    for i, (inputs, outputs) in enumerate(train_loader):
        predicted=predictor(inputs)
        loss=f_loss(predicted,outputs)
        loss.backward()
        optimizer.step()
        predictor.zero_grad()


from flask import Flask
from flask_ngrok import run_with_ngrok
from flask import request
  
app = Flask(__name__)
run_with_ngrok(app)
  

@app.route("/predict")
def predictor_invoke():
    lid = float(request.args.get('location_id'))
    day = float(request.args.get('day_number'))
    season = float(request.args.get('season_id'))
    temperature = float(request.args.get('temperature'))
    covid19 = float(request.args.get('cases'))

    sample=torch.tensor([[lid, day, season, temperature, covid19]])
    p_value=predictor(sample)
    response=str(predictions[0].item())
    return response
  
if __name__ == "__main__":
  app.run()