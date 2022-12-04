import torchvision
import pandas as pd
import numpy as np 
import torch
from torchvision import transforms
from PIL import Image
from matplotlib import pyplot as plt

if torch.cuda.is_available():
    use_cuda=True
else:
    use_cuda=False

# device = torch.device("cuda:0" if use_cuda else "cpu")
device = torch.device('cpu')

data_train = torchvision.datasets.FashionMNIST("data/FashionMNIST/resnet", train=True, transform=None, target_transform=None, download=True)
data_test = torchvision.datasets.FashionMNIST("data/FashionMNIST/resnet", train=False, transform=None, target_transform=None, download=True)

df_train = pd.DataFrame(np.hstack((data_train.train_labels.reshape(-1, 1), data_train.train_data.reshape(-1,28*28))))
df_test = pd.DataFrame(np.hstack((data_test.test_labels.reshape(-1, 1), data_test.test_data.reshape(-1,28*28))))

class_names = {
    0 : "T-shirt/top",
    1 : "Trouser",
    2 : "Pullover",
    3 : "Dress",
    4 : "Coat",
    5 : "Sandal",
    6 : "Shirt",
    7 : "Sneaker",
    8 : "Bag",
    9 : "Ankle boot"
}

def random_blackout(img, input_dim=(28, 28)):
    min_side = np.min(input_dim)
    high = np.round(min_side * .60)
    low = np.round(min_side * .15)
    # height, width
    h, w = np.random.randint(high=high, low=low, size=(2))

    # offsets top and left
    ofs_t = np.random.randint(high=input_dim[0]-h, low=0, size=1)[0]
    #ofs_t = 0
    ofs_l = np.random.randint(high=input_dim[1]-w, low=0, size=1)[0]
    #ofs_l = 0

    mask = np.ones(input_dim)

    mask[ofs_t:ofs_t+h,ofs_l:ofs_l+w] = 0

    return img * mask


class BlackoutTransform():
    def __init__(self):
        """
        """
        
    def __call__(self, img):
        img_dim = img.shape
        np_arr = img.view(28,28).numpy()
        np_arr = random_blackout(np_arr, np_arr.shape)
        return torch.FloatTensor(np_arr).view(img_dim)


class ReshapeTransform():
    def __init__(self, new_size):
        """
        :new_size: tuple
        """
        self.new_size = new_size

    def __call__(self, img):
        """Reshape an image
        :img: ex 1x28x28
        :returns: reshaped tensor
        """
        return torch.reshape(img, self.new_size)

t = transforms.Compose([transforms.RandomHorizontalFlip(p=0.5),
                        transforms.RandomVerticalFlip(p=0.5),
                        transforms.Pad((5,6)),
                        transforms.RandomCrop(size=28, padding_mode="reflect"),
                        #transforms.RandomCrop(size=28),
                        #transforms.RandomAffine([0,180], translate=None, scale=None, shear=None, resample=False, fillcolor=0),
                        # Resize random crop, then pad
                        #transforms.RandomResizedCrop(28, scale=(1.1, 1.3), ratio=(1.1, 1.5), interpolation=2),
                        transforms.Grayscale(num_output_channels=1),
                        transforms.ToTensor(),
                        BlackoutTransform(),
                        ReshapeTransform((1, 28, 28))
])
t_test = transforms.Compose([transforms.Pad((5,6)),
                        transforms.RandomCrop(size=28, padding_mode="reflect"),
                        transforms.Grayscale(num_output_channels=1),
                        transforms.ToTensor(),
                        BlackoutTransform(),
                        ReshapeTransform((1, 28, 28))
])

class CustomTensorDataset(torch.utils.data.TensorDataset):
    def __init__(self, *tensors, transforms=None):
        self.transform = transforms
        super().__init__(*tensors)
    
    def __getitem__(self, index):
        img, target = self.tensors[0][index], self.tensors[1][index]
        
        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        img = Image.fromarray(np.uint8(img.view(28,28).numpy()), mode='L')
    
        if self.transform is not None:
            img = self.transform(img)
                
        return (img, target)

def exclude_class(inputs, lbls, class_lbl):
    indices = np.where(lbls != class_lbl)
    inputs = np.take(inputs, indices[0], axis=0)
    lbls = np.take(lbls, indices[0], axis=0)
    return inputs, lbls

def show_images(images):
    n_images = len(images)
    w, h = 10, 10
    columns = 10
    rows = int(n_images / columns)
    fig=plt.figure(figsize=(columns*2, rows*2))
    for i in range(n_images):
        img = images[i].reshape(28,28)
        fig.add_subplot(rows, columns, i+1)
        plt.imshow(img, cmap='gray')
        plt.axis('off')
    plt.show()



# Train data
train_X = df_train.iloc[:,1:]
train_Y = df_train.iloc[:,:1]
# Test data
test_X = df_test.iloc[:,1:]
test_Y = df_test.iloc[:,:1]

train_X, train_Y = exclude_class(train_X, train_Y, 2)
test_X, test_Y = exclude_class(test_X, test_Y, 2)

# Normalize data to [0,1]
fmnist_train = torch.utils.data.TensorDataset(torch.FloatTensor(train_X.values/255).view(-1,1,28,28), torch.LongTensor(train_Y.values).view(-1))
fmnist_train = CustomTensorDataset(torch.FloatTensor(train_X.values), torch.LongTensor(train_Y.values).view(-1), transforms=t)
fmnist_test = torch.utils.data.TensorDataset(torch.FloatTensor(test_X.values/255).view(-1,1,28,28), torch.LongTensor(test_Y.values).view(-1))

# Batch size
batch_size = 256

train_loader = torch.utils.data.DataLoader(dataset=fmnist_train,
                                           batch_size=batch_size,
                                           pin_memory=True if use_cuda else False,
                                           shuffle=True) 
test_loader = torch.utils.data.DataLoader(dataset=fmnist_test,
                                          batch_size=batch_size,
                                          pin_memory=True if use_cuda else False,
                                          shuffle=False)

