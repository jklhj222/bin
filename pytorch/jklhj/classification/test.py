#!/usr/bin/env python3

import os
import torch as t
from torch.autograd import Variable
from torchvision.models import resnet152
from dataset import TestDataset
from config import DefaultConfig as DC

# read the defualt configure parameters
test_dir = DC.test_dir
test_model = DC.test_model
input_size = DC.input_size
num_workers = DC.num_workers
title_output = DC.title_output
normalize = DC.normalize

model = resnet152()
model.eval()

avgpool_kernel_size = 16
num_ftrs = model.fc.in_features
model.fc = t.nn.Linear(num_ftrs, 2)
model.avgpool = t.nn.AvgPool2d(avgpool_kernel_size, stride=1, padding=0)

if DC.use_gpu: model.cuda(DC.test_gpu_id)
#if DC.use_gpu: model.to('cuda:' + str(DC.test_gpu_id))

model.load_state_dict(t.load(test_model, 
                             map_location=lambda storage, 
                             loc: storage.cuda(DC.test_gpu_id)))

test_data = TestDataset(test_dir, resize=input_size, normalize=normalize)

test_dataloader = t.utils.data.DataLoader(test_data,
                                          batch_size=1,
                                          shuffle=False,
                                          num_workers=num_workers)

# for kaggle output
with open('test_predict.txt', 'w') as f:
    f.write(title_output + '\n')

for i, (data, img_path) in enumerate(test_dataloader):
    print(i, img_path)
    with t.no_grad():
        if DC.use_gpu:
            Input = Variable(data).cuda(DC.test_gpu_id)
            score = model(Input).cuda(DC.test_gpu_id)

        else:
            Input = Variable(data)
            score = model(Input)

        filename = os.path.basename(img_path[0])
        print('score: ', score)

        prob = t.nn.functional.softmax(score, dim=1)[:1].data.tolist()
        print('prob: ', prob, len(prob), '\n')

        with open('test_predict.txt', 'a') as f:
            f.write( filename + ',' + str(prob[0].index(max(prob[0]))) + '\n')

