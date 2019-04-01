from torchvision import transforms as T
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
                 normalize
                 ])
        
    def __getitem__(self, index):
        img_path = self.imgs[index]

        data = Image.open(img_path)
        data = self.transforms(data)

        return data, img_path

    def __len__(self):
        return len(self.imgs)

