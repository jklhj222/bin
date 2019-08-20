#!/usr/bin/env python3

import os
from torch.autograd import Variable
from torchvision.models import resnet152
from torchvision import transforms as T
from PIL import Image

from config import DefaultConfig as DC

def test(i, img, model):
    import torch as t
    # read the file with classes correspond to indices
    classes={}
    with open('classes.dat', 'r') as f:
        for line in f.readlines():
            classes[line.split(' ')[0]] = line.split(' ')[-1].replace('\n', '')

    # read the defualt configure parameters

    if DC.use_gpu: model.cuda(DC.test_gpu_id)

    input('test1')
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    model.to(t.device('cpu'))
#    model.to(t.device('cuda'))
#    input('test2')

    test_transforms = T.Compose([
             T.Resize((DC.input_size, DC.input_size)),
             T.ToTensor(),
             normalize
             ])

#    test_img = Image.open(DC.test_img)
    test_img = Image.open(img)
    test_img = test_transforms(test_img).unsqueeze(0)

    with t.no_grad():
        Input = Variable(test_img).cuda(DC.test_gpu_id)
        score = model(Input).cuda(DC.test_gpu_id)

    prob_all = t.nn.functional.softmax(score, dim=1)[:1].data.tolist()
    prob = max(prob_all[0])
    clas = prob_all[0].index(max(prob_all[0]))
    clas_name = classes[str(prob_all[0].index(max(prob_all[0])))]

    return [clas, clas_name, Input, score]

def test_loop():
    import torch as t
    input('enter 1')
    model = resnet152()
    model.eval()

    input('enter 2')
    num_ftrs = model.fc.in_features
    model.fc = t.nn.Linear(num_ftrs, DC.num_classes)

    input('enter 3')
    model.load_state_dict(t.load(test_model, 
                             map_location=lambda storage, 
                             loc: storage.cuda(DC.test_gpu_id)))

    input('enter 3.1')
    t.cuda.empty_cache()
#    del model    

    input('enter 3.2')
    for i, img in enumerate(['2019-06-26_10.44.52_0.31.jpg', '2019-06-26_12.20.10_0.9.jpg', '2019-07-26_09.35.44_0.4.jpg']):
        out = test(i, img, model)

        print('class :', out[0], out[1])
        input('enter 4')
        t.cuda.empty_cache()

#    device = t.device('cpu')
#    model.to(device)

    input('enter 5')
    del out[2]
    t.cuda.empty_cache()

    input('enter 6')

#    out[2] = None 
    del out[2]
    t.cuda.empty_cache()

    input('enter 7')
#    del model
    model = None
    t.cuda.empty_cache()

    input('enter 8')
    del t

    input('enter 9')


if __name__ == '__main__':
   
    test_model = DC.test_model
    input_size = DC.input_size
    normalize = DC.normalize


    print('loop 1')
    test_loop()
    print('loop 2')
    test_loop()
    print('loop 3')
    test_loop()
    print('loop 4')
    test_loop()

