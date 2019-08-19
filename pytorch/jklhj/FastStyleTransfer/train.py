#!/usr/bin/env python3

import torch as t
import torch.nn as nn
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
import tqdm

from transformer_net import TransformerNet
from PackedVGG import Vgg16
import utils
from config import DefaultConfig as DC

# mean and standard deviation of ImageNet
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

def train():
    train_gpu_id = DC.train_gpu_id
    device = t.device('cuda', train_gpu_id) if DC.use_gpu else t.device('cpu')

    transforms = T.Compose([
      T.Resize(DC.input_size),
      T.CenterCrop(DC.input_size),
      T.ToTensor(),
      T.Lambda(lambda x: x*255)
    ])

    train_dir = DC.train_content_dir
    batch_size = DC.train_batch_size

    train_data = ImageFolder(train_dir, transform=transforms)

    num_train_data = len(train_data)

    train_dataloader = t.utils.data.DataLoader(train_data,
                                               batch_size=batch_size,
                                               shuffle=True,
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

    # Get the data from style image
    ys = utils.get_style_data(DC.style_img)
    ys = ys.to(device)

    # The Gram matrix of the style image
    with t.no_grad():
        features_ys = vgg(ys)

        gram_ys = [utils.gram_matrix(ys) for ys in features_ys]

    # Start training
    train_imgs = 0
    iteration = 0
    for epoch in range(DC.max_epoch):
        for i, (data, label) in tqdm.tqdm(enumerate(train_dataloader)):
            train_imgs += batch_size
            iteration += 1

            optimizer.zero_grad()
         
            # Transformer net
            x = data.to(device)
            y = transformer(x)

            x = utils.normalize_batch(x)
            yc = x
            y = utils.normalize_batch(y)

            features_y = vgg(y)
            features_yc = vgg(yc)

            # Content loss
            content_loss = DC.content_weight * \
                             nn.functional.mse_loss(features_y.relu2_2, 
                                                    features_yc.relu2_2)
#            content_loss = DC.content_weight * \
#                             nn.functional.mse_loss(features_y.relu3_3, 
#                                                    features_yc.relu3_3)

            # Style loss
            style_loss = 0.0
            for ft_y, gm_ys in zip(features_y, gram_ys):
                gm_y = utils.gram_matrix(ft_y)
                
                style_loss += nn.functional.mse_loss(gm_y, 
                                                     gm_ys.expand_as(gm_y))


            style_loss *= DC.style_weight

            # Total loss
            total_loss = content_loss + style_loss
            total_loss.backward()
            optimizer.step()

            if iteration%DC.show_iter == 0: 
                print('\ncontent loss: ', content_loss.data)
                print('style loss: ', style_loss.data)
                print('total loss: ', total_loss.data)
                print()

        t.save(transformer.state_dict(), '{}_style.pth'.format(epoch))

if __name__ == '__main__':
    train()
