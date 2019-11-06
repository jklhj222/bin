from torchvision import transforms as T
from torchvision.datasets import ImageFolder
from torch.utils import data
from PIL import Image
import os

# for the testing images all in a directory,
# returns image data and file name.
class TestDataset(data.Dataset):
    def __init__(self, data_path, normalize, resize=224):

        imgs = [os.path.join(data_path, img) for img in os.listdir(data_path)]

        imgs = sorted(imgs)

        self.imgs = imgs

        self.transforms = T.Compose([
                 T.Resize((resize, resize)),
                 T.ToTensor(),
#                 normalize
                 ])
        
    def __getitem__(self, index):
        img_path = self.imgs[index]

        data = Image.open(img_path)
        img_width  = data.size[0]
        img_height = data.size[1]
        print(img_width, img_height)

        data = self.transforms(data)

        return data, img_path, img_width, img_height

    def __len__(self):
        return len(self.imgs)


class ValImageFolder(ImageFolder):
    def __getitem__(self, index):

        # original ImageFolder normally returns
        original_tuple = super(ValImageFolder, self).__getitem__(index)

        # image file path
        path = self.imgs[index][0]

        tuple_with_path = (original_tuple + (path, ))

        return tuple_with_path
