from torchvision import transforms as T
from torch.utils import data
from PIL import Image
import os

# for the testing images all in a directory,
# returns image data and file name.
class TestDataset(data.Dataset):
    def __init__(self, data_path, resize=224):

        imgs = [os.path.join(data_path, img) for img in os.listdir(data_path)]

        imgs = sorted(imgs)

        self.imgs = imgs

        self.transforms = T.Compose([
                 T.Resize((resize, resize)),
                 T.ToTensor(),
#                 T.Normalize(mean=[0.503285495691, 0.451637785218, 0.467750980149],
#                              std=[0.151216848168, 0.139701434141, 0.153258293707])
                 ])
        
    def __getitem__(self, index):
        img_path = self.imgs[index]

        data = Image.open(img_path)
        data = self.transforms(data)

        return data, img_path

    def __len__(self):
        return len(self.imgs)

