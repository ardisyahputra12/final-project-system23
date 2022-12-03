from torch import nn
from torch.nn.parameter import Parameter
import torch.optim as optim
from app.utils.classification.preprocesing import device
from app.utils.classification.resnet import ResNet, ResnetBlock
import torch

def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.xavier_normal_(m.weight.data)

## Initialize model
model = ResNet(ResnetBlock, [2,2,2,2], k=2)

# Initialize linear layers
model.apply(init_weights)

# load pretrained state
model.to(device)
model.load_state_dict(torch.load("/app/utils/classification/test_acc-8102-epoch19.pth"))
# model.load_state_dict(torch.load("models\\training.pt"))

# Loss fn
criterion = nn.CrossEntropyLoss()

# optimizer and scheduler
optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=0.0001, momentum=0.9)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', min_lr=1e-4, patience=8, verbose=True)

# only save model state if test acc is above "best_test_acc"
best_test_acc = 9560

# Use dramatic increased LR every x'th epoch (0 = None)
lr_inc_interval = 40