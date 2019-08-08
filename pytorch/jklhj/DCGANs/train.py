#!/usr/bin/env python3

import torch as t
import torchvision as tv
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
import tqdm

from config import DefaultConfig as DC
import model

device = t.device('cuda') if DC.use_gpu else t.device('cpu')

transform = T.Compose([
        T.Resize((DC.input_size, DC.input_size)),
        T.CenterCrop(DC.input_size),
        T.ToTensor(),
        T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

train_dir = DC.train_dir
batch_size = DC.train_batch_size

train_data = ImageFolder(train_dir, transform=transform)

num_train_data = len(train_data)

train_dataloader = t.utils.data.DataLoader(train_data,
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=DC.num_workers,
                                           drop_last=True)

netg = model.NetG(DC)
netd = model.NetD(DC)

if DC.train_netg_model: 
    netg.load_state_dict(t.load(DC.train_netg_model,
                                map_location=lambda storage, loc: storage))

if DC.train_netd_model: 
    netd.load_state_dict(t.load(DC.train_netd_model,
                                map_location=lambda storage, loc: storage))

netg.to(device)
netd.to(device)

# optimizer and loss function
optimizer_g = t.optim.Adam(netg.parameters(), 
                           lr=DC.base_lrg, 
                           betas=(DC.adam_beta1, 0.999))
optimizer_d = t.optim.Adam(netd.parameters(), 
                           lr=DC.base_lrd, 
                           betas=(DC.adam_beta1, 0.999))

criterion = t.nn.BCELoss().to(device)

#scheduler = t.optim.lr_scheduler.StepLR()

true_labels = t.ones(batch_size).to(device)
fake_labels = t.zeros(batch_size).to(device)
fix_noises = t.randn(batch_size, DC.nz, 1, 1).to(device)
noises = t.randn(batch_size, DC.nz, 1, 1).to(device)

train_imgs = 0
iteration = 0
for epoch in range(DC.max_epoch):
    print('epoch: ', epoch, 'iter: ', iteration)
    for i, (data, label) in tqdm.tqdm(enumerate(train_dataloader)):
        train_imgs += batch_size
        iteration += 1

        if i % DC.g_train_every == 0:
            optimizer_g.zero_grad()

#            noises.data.copy_(t.randn(bathc_size, DC.nz, 1, 1))
            fake_img = netg(noises)
            output = netd(fake_img)

            loss_g = criterion(output, true_labels)

            loss_g.backward()

            optimizer_g.step()

        real_data = data.to(device)
        if i % DC.d_train_every == 0:
            optimizer_d.zero_grad()

            # discriminate the real picture as True as possible
            output = netd(real_data)
            loss_d_real = criterion(output, true_labels)
            loss_d_real.backward()

            # discriminate the fake picture as False as possible
            noises.data.copy_(t.randn(batch_size, DC.nz, 1, 1))
            fake_data = netg(noises).detach()

            output = netd(fake_data)
            loss_d_fake = criterion(output, fake_labels)
            loss_d_fake.backward()
            
            optimizer_d.step()

            loss_d = loss_d_fake + loss_d_real

        if iteration % DC.save_iter == 0:
            fix_fake_imgs = netg(fix_noises)
            tv.utils.save_image(fix_fake_imgs.data[:64], 
                                '{:s}/iter{:d}_epoch{}.png'.format(DC.pic_save_dir, 
                                                       iteration, epoch),
                                normalize=True, 
                                range=(-1, 1))

            t.save(netg.state_dict(), 'netg_iter{}_epoch{}.pth'.format(iteration, epoch+1))
            t.save(netd.state_dict(), 'netd_iter{}_epoch{}.pth'.format(iteration, epoch+1))

    print('loss_g: ', loss_g, 'loss_d', loss_d, 'netd_output: ', output[:100])
