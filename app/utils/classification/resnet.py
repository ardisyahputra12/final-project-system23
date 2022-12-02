from torch import nn

# Create helper functions to resnet blocks
def conv1x1(in_planes, out_planes,stride=1):
    """1x1 convolutional"""
    return nn.Conv2d(in_planes,out_planes,kernel_size=1,stride=1,bias=False)

def conv3x3(in_planes, out_planes,stride=1):
    """3x3 convolutional """
    return nn.Conv2d(in_planes,out_planes,kernel_size=3,stride=1,padding=1,bias=False)

class ResnetBlock(nn.Module):
    expansion = 1
    
    def __init__(self, in_planes, out_planes, stride=1, downsample=None, dropout=0.18):
        super(ResnetBlock, self).__init__()
        # Conv layer 1
        self.conv_1 = conv3x3(in_planes, out_planes, stride)
        self.batch_norm_1 = nn.BatchNorm2d(out_planes)
        self.relu = nn.ReLU(inplace=True)
        self.dropout = dropout
        if self.dropout:
            self.dropout1 = nn.Dropout(p=dropout)
        # Conv layer 2
        self.conv_2 = conv3x3(out_planes, out_planes)
        self.batch_norm_2 = nn.BatchNorm2d(out_planes)
        self.downsample = downsample
        self.stride = stride
        
    def forward(self, x):
        residual = x
        
        out = self.conv_1(x)
        # If no dropout then use batchnorm
        if not self.dropout:
            out = self.batch_norm_1(out)
        out = self.relu(out)
        
        # Use dropout in between
        if self.dropout:
            out = self.dropout1(out)
        
        out = self.conv_2(out)
        out = self.batch_norm_2(out)
        
        if self.downsample is not None:
            residual = self.downsample(x)
        
        out += residual
        out = self.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=10, k=1):
        super(ResNet, self).__init__()
        self.inplanes = 64
        # Convert to 64 channels
        self.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=1, padding=3, bias=False)  # out bx64x28x28
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)  # out bx64x14x14
        self.layer1 = self._make_layer(block, 64*k, layers[0])  # out bx(64xk)x14x14
        self.layer2 = self._make_layer(block, 128*k, layers[1], stride=2)  # out bx(128xk)x7x7
        #self.layer3 = self._make_layer(block, 256*k, layers[2], stride=2)
        #self.layer4 = self._make_layer(block, 512*k, layers[3], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))  # out bx(128*k)x1x1
        self.fc = nn.Linear(128*k * block.expansion, num_classes)  # out bx10

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                #nn.init.xavier_normal_(m.weight)
                
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                conv1x1(self.inplanes, planes * block.expansion, stride),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        #x = self.layer3(x)
        #x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x