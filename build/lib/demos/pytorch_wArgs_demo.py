import torch
import torch.nn as nn

from torch.optim import Adam, SGD
from math import pi

from wArgs import wildArgs, wArgs, wArgsCall, wArgsClass, wArgsChk, wArgsInit, struct

wArgsInit(globals())

class myModel(nn.Module):
    def __init__(self, nLayers=3,
                 nInputNeurons=5, nHiddenNeurons=10, nOutputNeurons=2,
                 actv=nn.Tanh,
                 pool=nn.MaxPool1d, poolsz=2,
                 dropout=nn.Dropout, alpha=.15, **kwargs):
        nn.Module.__init__(self)

        self.layers = []
        self.layers.append(nn.Linear(nInputNeurons, nHiddenNeurons))
        if actv:
            self.layers.append(actv())
        if pool:
            self.layers.append(pool(poolsz))
        if dropout:
            self.layers.append(dropout(alpha))
            
        for i in range(nLayers):
            self.layers.append(nn.Linear(nHiddenNeurons, nHiddenNeurons))
            if actv:
                self.layers.append(actv())
            if pool:
                self.layers.append(pool(poolsz))
            if dropout:
                self.layers.append(dropout(alpha))

        self.layers.append(nn.Linear(nHiddenNeurons, nOutputNeurons))
        if actv:
            self.layers.append(actv())
        if pool:
            self.layers.append(pool(poolsz))
        if dropout:
            self.layers.append(dropout(alpha))

        self.model = nn.Sequential(*self.layers)

    def forward(self, x):
        return self.model()


myModelwArgsC = wArgsClass(myModel)    # Grabs args from parent classes
optmC = wArgs(Adam)                    # Only child class
wArgsChk()  # warn=True)

model = myModelwArgsC()
optm=optmC(model.parameters())
print(model)
print(optm)
