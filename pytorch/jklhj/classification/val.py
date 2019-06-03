#!/usr/bin/env python3

from torch.autograd import Variable
import torch as t
from config import DefaultConfig as DC

def val(in_train, model, transform, val_data, dataloader):
    model.eval()    

    val_transform = transform
    
    num_val_data = len(val_data)
    
    val_dataloader = dataloader

    # resetting the model 
    if not in_train:    
        avgpool_kernel_size = 16
        num_ftrs = model.fc.in_features
        model.fc = t.nn.Linear(num_ftrs, num_classes)
        model.avgpool = t.nn.AvgPool2d(avgpool_kernel_size, stride=1, padding=0)
    
    if DC.use_gpu:
        if not in_train: 
            model.to('cuda:' + str(DC.val_gpu_id))

    if not in_train: model.load_state_dict(
                       t.load(DC.val_model,
                              map_location=lambda storage,
                              loc: storage.cuda(DC.val_gpu_id)))
    
    criterion = t.nn.CrossEntropyLoss()
    
    model.eval()
    avg_loss = 0
    total_img = 0 
    correct_img = 0
    
    for i, (data, label) in enumerate(val_dataloader):
        with t.no_grad():
            if DC.use_gpu:
                if not in_train:
                    Input = Variable(data).cuda(DC.val_gpu_id)
                    target = Variable(label).cuda(DC.val_gpu_id)
                    score = model(Input).cuda(DC.val_gpu_id)
 
                else:    
                    Input = Variable(data).cuda(DC.train_gpu_id)
                    target = Variable(label).cuda(DC.train_gpu_id)
                    score = model(Input).cuda(DC.train_gpu_id)

            else:
                Input = Variable(data)
                target = Variable(label)
                score = model(Input)
   
            testimg = val_data.imgs
#            print(testimg, type(testimg))
 
            loss = criterion(score, target)
            avg_loss = (avg_loss*i*DC.val_batch_size + loss.item()) \
                         / (DC.val_batch_size*(i+1))
    
            prob = t.nn.functional.softmax(score, dim=1)[:1].data.tolist()
    
            total_img += 1
            if label.tolist()[0] == prob[0].index(max(prob[0])):
                correct_img += 1

            if not in_train:
                print('{}/{} {}  {}'.format(i+1, 
                                            num_val_data, 
                                            prob[0].index(max(prob[0])),
                                            prob))
    
    accuracy = (correct_img/total_img)*100

    if not in_train:    
        print(' Avg_loss: {:.8f}\n'.format(avg_loss),
              'Accuracy:({}/{}) {:.4f}% '.format(correct_img, 
                                                 total_img, 
                                                 accuracy))

    return (avg_loss, correct_img, total_img, accuracy)

if __name__ == '__main__':
    from torchvision.models import resnet152
    from torchvision import transforms as T
    from torchvision.datasets import ImageFolder

    model = resnet152(pretrained=False)
   
    val_transform = T.Compose([
            T.Resize(DC.input_size),
            T.ToTensor(),
            DC.normalize])
    
    val_data = ImageFolder(DC.val_dir,
                           transform=val_transform)

    val_dataloader = t.utils.data.DataLoader(val_data,
                                             batch_size=DC.val_batch_size,
                                             shuffle=False,
                                             num_workers=DC.num_workers)

    val(False, model, val_transform, val_data, val_dataloader)


