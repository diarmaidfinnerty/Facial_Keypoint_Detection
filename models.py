## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        
        self.conv1 = nn.Conv2d(1, 32, 7, 3, 1)       ## output size = (W-F+2P)/S +1 = (224-7+2)/3 +1 = 74
        self.conv2 = nn.Conv2d(32, 64, 5, 3, 0)      ## output size = (W-F+2P)/S +1 = (74-5)/3 +1 = 24
        self.conv3 = nn.Conv2d(64, 128, 5, 3, 1)     ## output size = (24-5+2)/3 +1 = 8
        self.conv4 = nn.Conv2d(128, 256, 3, 1, 0)    ## output size = (8-3)/1 +1 = 6
        self.conv5 = nn.Conv2d(256, 512, 3, 1, 0)    ## output size = (6-3)/1 +1 = 4
        self.conv6 = nn.Conv2d(512, 512, 1, 1, 0)    ## output size = (4-1)/1 +1 = 4
        
        self.fc1 = nn.Linear(4*4*512, 1024)
        self.fc1_drop = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(1024, 1024)
        self.fc2_drop = nn.Dropout(p=0.4)
        self.fc3 = nn.Linear(1024, 1024)
        self.fc3_drop = nn.Dropout(p=0.3)
        self.fc4 = nn.Linear(1024, 1024)
        self.fc4_drop = nn.Dropout(p=0.2)
        self.fc5 = nn.Linear(1024, 1024)
        self.fc5_drop = nn.Dropout(p=0.1)
        self.fc6 = nn.Linear(1024, 136)

        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        
        # Apply convolutional layers
        x = F.selu(self.conv1(x))
        x = F.selu(self.conv2(x))
        x = F.selu(self.conv3(x))
        x = F.selu(self.conv4(x))
        x = F.selu(self.conv5(x))
        x = F.selu(self.conv6(x))

        # Flatten and continue with dense layers
        x = x.view(x.size(0), -1)
        x = F.selu(self.fc1(x))
        x = self.fc1_drop(x)
        x = F.selu(self.fc2(x))
        x = self.fc2_drop(x)
        x = F.selu(self.fc3(x))
        x = self.fc3_drop(x)
        x = F.selu(self.fc4(x))
        x = self.fc4_drop(x)
        x = F.selu(self.fc5(x))
        x = self.fc5_drop(x)
        x = self.fc6(x)
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x