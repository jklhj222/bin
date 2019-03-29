#!/usr/bin/env python3

import torch as t
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
from torchvision.models import resnet152
from torch.autograd import Variable
import time
import os, sys

from config import DefaultConfig as DC
import val

train_transform = T.Compose([
        T.Resize(DC.input_size),
#        T.RandomResizedCrop(224),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.ToTensor(),
        DC.normalize,
        ])
        

train_dir = DC.train_dir

train_data = ImageFolder(train_dir, 
                         transform=train_transform)

num_train_data = len(train_data)

train_dataloader = t.utils.data.DataLoader(train_data,
                                           batch_size=DC.train_batch_size,
                                           shuffle=True,
                                           num_workers=DC.num_workers)

if DC.val_in_train:
    val_transform = T.Compose([
            T.Resize(DC.input_size),
#            T.RandomResizedCrop(224),
            T.ToTensor(),
            DC.normalize
            ])

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
model = resnet152(pretrained=DC.pretrained)

avgpool_kernel_size = 16 
num_ftrs = model.fc.in_features
model.fc = t.nn.Linear(num_ftrs, 2)
model.avgpool = t.nn.AvgPool2d(avgpool_kernel_size, stride=1, padding=0)

if DC.use_gpu: model.cuda(DC.train_gpu_id)

train_imgs = 0
iteration = 0
start_epoch = 0
if DC.load_model: 
    model.load_state_dict(t.load(DC.load_model))
    iteration = int(DC.load_model.split('.')[0].split('iter')[1])

    start_epoch = int(iteration*DC.train_batch_size/num_train_data)-1
    train_imgs = iteration * DC.train_batch_size

print(dir(model))
for i in DC.__dict__.items():
    print(i)

print()
print('Number of training data:', num_train_data)
if DC.val_in_train: print('Number of val data:', len(val_data), '\n')

criterion = t.nn.CrossEntropyLoss()

optimizer = t.optim.Adam(model.parameters(), lr=DC.base_lr) 
#optimizer = t.optim.SGD(model.parameters(), lr=DC.base_lr, momentum=0.9) 

scheduler = t.optim.lr_scheduler.StepLR(optimizer, 
                                        step_size=DC.lr_decay_step, 
                                        gamma=0.1)

time0 = time.time()
score_list = []
target_list = []
for epoch in range(start_epoch, DC.max_epoch):
    model.train()
#    print('model training: ', model.training)
    scheduler.step()

    avg_loss = 0
    for i, (data, label) in enumerate(train_dataloader):
        train_imgs += DC.train_batch_size
        iteration += 1

        if DC.use_gpu:
            Input = Variable(data).cuda(DC.train_gpu_id)
            target = Variable(label).cuda(DC.train_gpu_id)
            score = model(Input).cuda(DC.train_gpu_id)

        else:
            Input = Variable(data)
            target = Variable(label)
            score = model(Input)

        optimizer.zero_grad()
        loss = criterion(score, target)
        avg_loss = (avg_loss * i * DC.train_batch_size + loss.item()) \
                     / (DC.train_batch_size*(i+1))

        loss.backward()
        optimizer.step()
        lr = optimizer.param_groups[0]['lr']
        
        score_list.extend(score.tolist())
        target_list.extend(target.tolist())

        if (iteration%DC.show_iter==0): 
            # compute accuracy for showing process        
            total_img = 0
            correct_img = 0
            for i, j in zip(score_list, target_list):
                if i.index(max(i)) == j:
                    correct_img += 1
                total_img += 1

            accuracy = (correct_img/total_img)*100

            elps_time = time.time() - time0
            time0 = time.time()
            score_list = []
            target_list = []
            print('epoch:', epoch, 
                  ' iter:', iteration, 
                  ' avg loss: {:.6f}'.format(float(avg_loss)),
                  ' acc:({}/{}) {:.2f}%'.format(correct_img, 
                                                total_img, 
                                                accuracy),
                  ' lr:', lr,
                  ' time/iter: {:.2f}'.format(elps_time/DC.show_iter), 's/iter',
                  ' time: {:.2f}'.format(elps_time), 's',
                  ' images:', train_imgs, ',',
                  ' {:.1f}'.format((DC.show_iter*DC.train_batch_size) / 
                                  (elps_time)), 'img/s')

        if os.path.isfile('STOPCAR'):
            t.save(model.state_dict(), 'ResNet101-iter'+str(iteration)+'.pth')
            os.remove('STOPCAR')
            sys.exit()

        if (iteration%DC.save_iter==0) or (epoch == DC.max_epoch):
            t.save(model.state_dict(), 'ResNet101-iter'+str(iteration)+'.pth')

        if os.path.isfile('SAVENOW'):
            t.save(model.state_dict(), 'ResNet101-iter'+str(iteration)+'.pth')
            os.remove('SAVENOW')

        if DC.val_in_train and iteration%DC.val_iter==0:
#            print('model.training: ', model.training)
            time1 = time.time()

            val_out = val.val(True, model, val_transform, val_data, val_dataloader)

            model.train()

            val_elps_time = time.time() - time1

            print('Validate now, ', 
                  ' epoch:', epoch,
                  ' iter:', iteration, 
                  ' avg loss: {:.8f}'.format(val_out[0]),
                  ' accuracy:({}/{}) {:.4f}% '.format(val_out[1], 
                                                      val_out[2], 
                                                      val_out[3]),
                  ' time: {:.3f}'.format(val_elps_time))
