#!/usr/bin/env python3

import torch as t
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
from torchvision.models import resnet101
from torch.autograd import Variable
import time
import os, sys

from config import DefaultConfig as DC

train_transform = T.Compose([
#        T.Resize(32),
#        T.RandomResizedCrop(224),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.ToTensor()])

train_dir = DC.train_dir

train_data = ImageFolder(train_dir, 
                         transform=train_transform)

train_dataloader = t.utils.data.DataLoader(train_data,
                                           batch_size=DC.train_batch_size,
                                           shuffle=True,
                                           num_workers=DC.num_workers)

if DC.val:
    val_transform = T.Compose([
#            T.Resize(224),
#            T.RandomResizedCrop(224),
            T.ToTensor()])

    val_dir = DC.val_dir

    val_data = ImageFolder(val_dir,
                           transform=val_transform)

    val_dataloader = t.utils.data.DataLoader(val_data,
                                             batch_size=DC.val_batch_size,
                                             shuffle=False,
                                             num_workers=DC.num_workers)


classes = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
classes.sort()
with open('classes.dat', 'w') as f:
    for i, clas in enumerate(classes):
        f.write(str(i) + ' : ' + str(clas) + '\n')

# model setting
model = resnet101(pretrained=DC.pretrained)

avgpool_kernel_size = 1 
num_ftrs = model.fc.in_features
model.fc = t.nn.Linear(num_ftrs, 2)
model.avgpool = t.nn.AvgPool2d(avgpool_kernel_size, stride=1, padding=0)

if DC.use_gpu: model.cuda(DC.gpu_id)

if DC.pretrained: model.load_state_dict(td.load(DC.load_model))

print(dir(model), '\n')
for i in DC.__dict__.items():
    print(i)

criterion = t.nn.CrossEntropyLoss()

optimizer = t.optim.SGD(model.parameters(), lr=DC.base_lr, momentum=0.9) 

scheduler = t.optim.lr_scheduler.StepLR(optimizer, 
                                        step_size=DC.lr_decay_step, 
                                        gamma=0.1)

train_imgs = 0
iteration = 0
for epoch in range(DC.max_epoch):
    model.train()
#    print('model training: ', model.training)
    scheduler.step()

    avg_loss = 0
    for i, (data, label) in enumerate(train_dataloader):
        time0 = time.time()
        train_imgs += DC.train_batch_size
        iteration += 1

        if DC.use_gpu:
            Input = Variable(data).cuda(DC.gpu_id)
            target = Variable(label).cuda(DC.gpu_id)
            score = model(Input).cuda(DC.gpu_id)

        else:
            Input = Variable(data)
            target = Variable(label)
            score = model(Input)

        optimizer.zero_grad()
        loss = criterion(score, target)
        avg_loss = (avg_loss * i * DC.train_batch_size + loss) \
                     / (DC.train_batch_size*(i+1))

        loss.backward()
        optimizer.step()
        lr = optimizer.param_groups[0]['lr']

        elps_time = time.time() - time0
        if (iteration%DC.show_iter==0): 
            print('epoch:', epoch, 
                  ' iter:', iteration, 
                  ' avg loss: {:.6f}'.format(float(avg_loss)),
                  ' lr:', lr,
                  ' elpsed time/iter: {:.3f}'.format(elps_time), 's',
                  ' elpsed time: {:.3f}'.format(elps_time*DC.show_iter), 's',
                  ' train images:', train_imgs, ',',
                  ' {:.1f}'.format((DC.show_iter*DC.train_batch_size) / 
                                  (elps_time*DC.show_iter)), 'img/s')

        if os.path.isfile('STOPCAR'):
            t.save(model.state_dict(), 'ResNet101-iter'+str(iteration)+'.pth')
            os.remove('STOPCAR')
            sys.exit()

        if (iteration%DC.save_iter==0) or os.path.isfile('SAVENOW'):
            t.save(model.state_dict(), 'ResNet101-iter'+str(iteration)+'.pth')

        if os.path.isfile('SAVENOW'):
            t.save(model.state_dict(), 'ResNet101-iter'+str(iteration)+'.pth')
            os.remove('SAVENOW')

        if DC.val and iteration%DC.val_iter==0:
            model.eval()
            avg_loss = 0
#            print('model.training: ', model.training)
            for i, (data, label) in enumerate(val_dataloader):
           
                if DC.use_gpu:
                    Input = Variable(data).cuda(DC.gpu_id)
                    target = Variable(label).cuda(DC.gpu_id)
                    score = model(Input).cuda(DC.gpu_id)

                else:
                    Input = Variable(data)
                    target = Variable(label)
                    score = model(Input)

                loss = criterion(score, target) 
                avg_loss = (avg_loss * i * DC.val_batch_size + loss) \
                             / (DC.train_batch_size*(i+1))

            print('Validate now, ', 
                  'epoch: ', epoch+1,
                  'iter: ', iteration, 
                  'avg loss: {:.12f}'.format(float(avg_loss)),
                  'train images: ', train_imgs)
