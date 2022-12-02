import torch

from inference import make_predictions
from preprocesing import device, t_test, test_loader
from resnet import ResNet, ResnetBlock, conv1x1, conv3x3

# Load model
model = ResNet(ResnetBlock, [2,2,2,2], k=2)
model.load_state_dict(torch.load("test_acc-8102-epoch19.pth"))
model = model.to(device)

total_wrong_labels = torch.LongTensor().cuda()
model.eval()
with torch.no_grad():
    for i, data in enumerate(test_loader):
        # inputs
        inputs, labels = data[0].to(device), data[1].to(device)
        outputs = model(inputs)

        # correct
        test_correct = outputs.argmax(-1).eq(labels)
        wrong_labels = labels[test_correct == 0]
        total_wrong_labels = torch.cat((total_wrong_labels, wrong_labels))

test_labels=data[1][:9]
test_samples = data[0][:9]

# Make predictions on test samples with model 0
pred_probs= make_predictions(model=model, 
                             data=test_samples)

pred_classes = pred_probs.argmax(dim=1)

y_class =['T-shirt/top',
 'Trouser',
 'Pullover',
 'Dress',
 'Coat',
 'Sandal',
 'Shirt',
 'Sneaker',
 'Bag',
 'Ankle boot']

dummy = y_class[pred_classes[0]]

# test jurry test
import torch
from PIL import Image

images = Image.open("data\Jury Test Set\mnist_58.png")
img_transform  =t_test(images)
img_transform = torch.FloatTensor(img_transform).view(-1,1,28,28)

y_probs = make_predictions(model,img_transform)
y_preds = y_probs.argmax(axis=1)
print(y_class[y_preds])