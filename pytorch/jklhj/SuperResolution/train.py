#!/usr/bin/env python3

import torch as t
import torch.nn as nn
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
import tqdm

from transformer_net import TransformerNet
from PackedVGG import Vgg16
import utils

# mean and standard deviation of ImageNet
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]


def train(DC):
    train_gpu_id = DC.train_gpu_id
    device = t.device('cuda', train_gpu_id) if DC.use_gpu else t.device('cpu')

    input_size = DC.input_size
    super_resol_factor = DC.super_resol_factor

    high_transforms = T.Compose([
      T.Resize(input_size),
      T.CenterCrop(input_size),
      T.ToTensor(),
      T.Lambda(lambda x: x*255)
    ])
    low_transforms = T.Compose([
      T.Resize(int(input_size/super_resol_factor)),
      T.CenterCrop(int(input_size/super_resol_factor)),
      T.ToTensor(),
      T.Lambda(lambda x: x*255)
    ])

    HighResol_dir = DC.HighResol_dir
    LowResol_dir = DC.LowResol_dir
    batch_size = DC.train_batch_size

    HighResol_data = ImageFolder(HighResol_dir, transform=high_transforms)
    LowResol_data = ImageFolder(LowResol_dir, transform=low_transforms)

    num_train_data = len(HighResol_data)

    HighResol_dataloader = t.utils.data.DataLoader(HighResol_data,
                                                   batch_size=batch_size,
                                                   shuffle=False,
                                                   num_workers=DC.num_workers,
                                                   drop_last=True)

    LowResol_dataloader = t.utils.data.DataLoader(LowResol_data,
                                                  batch_size=batch_size,
                                                  shuffle=False,
                                                  num_workers=DC.num_workers,
                                                  drop_last=True)
    # transform net
    transformer = TransformerNet()
    if DC.load_model:
        transformer.load_state_dict(
          t.load(DC.load_model, 
                 map_location=lambda storage, loc: storage))

    transformer.to(device)

    # Loss net (vgg16)
    vgg = Vgg16().eval()
    vgg.to(device)

    for param in vgg.parameters():
        param.requires_grad = False

    optimizer = t.optim.Adam(transformer.parameters(), DC.base_lr)

    # Start training
    train_imgs = 0
    iteration = 0
    for epoch in range(DC.max_epoch):
        for i, ((high_data, _), (low_data, _)) in tqdm.tqdm(
                                               enumerate(
                                               zip(HighResol_dataloader, 
                                                   LowResol_dataloader))):

            train_imgs += batch_size
            iteration += 1

            optimizer.zero_grad()
         
            # Transformer net
            x = low_data.to(device)
            y = transformer(x)
            y = utils.normalize_batch(y)

            yc = high_data.to(device)
            yc = utils.normalize_batch(yc)
 
            features_y = vgg(y)
            features_yc = vgg(yc)

            # Content loss
            content_loss = DC.content_weight * \
                             nn.functional.mse_loss(features_y.relu2_2, 
                                                    features_yc.relu2_2)
#            content_loss = DC.content_weight * \
#                            nn.functional.mse_loss(features_y.relu3_3, 
#                                                   features_yc.relu3_3)

            content_loss.backward()
            optimizer.step()

            if iteration%DC.show_iter == 0: 
                print('\nepoch: ', epoch)
                print('content loss: ', content_loss.data)
                print()

        if (epoch+1)%10 == 0: t.save(transformer.state_dict(), '{}_style.pth'.format(epoch))

if __name__ == '__main__':
    from config import DefaultConfig as DC

    train(DC)
