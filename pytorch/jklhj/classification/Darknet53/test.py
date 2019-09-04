#!/usr/bin/env python3

import os
import torch as t
from torch.autograd import Variable

from dataset import TestDataset
from config import DefaultConfig as DC
from model import Darknet53

# read the defualt configure parameters
test_dir = DC.test_dir
test_model = DC.test_model
input_size = DC.input_size
num_workers = DC.num_workers
title_output = DC.title_output
normalize = DC.normalize

model = Darknet53(num_classes=DC.num_classes, 
                  bias=True)
model.eval()

if DC.use_gpu: model.cuda(DC.test_gpu_id)
#if DC.use_gpu: model.to('cuda:' + str(DC.test_gpu_id))

model.load_state_dict(t.load(test_model, 
                             map_location=lambda storage, 
                             loc: storage.cuda(DC.test_gpu_id)))

test_data = TestDataset(test_dir, normalize=normalize, resize=input_size)

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
        print('prob: ', prob, prob[0].index(max(prob[0])), '\n')

        with open('test_predict.txt', 'a') as f:
            f.write( filename + ',' + str(prob[0].index(max(prob[0]))) + '\n')

