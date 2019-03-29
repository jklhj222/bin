import torch as t
from torchvision import transforms as T
from torchvision.datasets import ImageFolder
from torch.autograd import Variable
from torchvision.models import resnet152
from config import DefaultConfig as DC

val_dir = DC.val_dir

val_transform = T.Compose([
        T.Resize(DC.input_size),
#        T.RandomResizedCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.503285495691, 0.451637785218, 0.467750980149],
                     std=[0.151216848168, 0.139701434141, 0.153258293707])
        ])

val_data = ImageFolder(val_dir,
                       transform=val_transform)

num_val_data = len(val_data)

val_dataloader = t.utils.data.DataLoader(val_data,
                                         batch_size=DC.val_batch_size,
                                         shuffle=False,
                                         num_workers=DC.num_workers)

model = resnet152(pretrained=False)

#avgpool_kernel_size = 16
num_ftrs = model.fc.in_features
model.fc = t.nn.Linear(num_ftrs, 2)
#model.avgpool = t.nn.AvgPool2d(avgpool_kernel_size, stride=1, padding=0)

if DC.use_gpu: model.cuda(DC.val_gpu_id)

model.load_state_dict(t.load(DC.val_model))

criterion = t.nn.CrossEntropyLoss()

model.eval()
avg_loss = 0
total_img = 0 
correct_img = 0

for i, (data, label) in enumerate(val_dataloader):
    with t.no_grad():
        if DC.use_gpu:
            Input = Variable(data).cuda(DC.val_gpu_id)
            target = Variable(label).cuda(DC.val_gpu_id)
            score = model(Input).cuda(DC.val_gpu_id)

        else:
            Input = Variable(data)
            target = Variable(label)
            score = model(Input)

        loss = criterion(score, target)
        avg_loss = (avg_loss*i*DC.val_batch_size + loss.item()) \
                     / (DC.val_batch_size*(i+1))

        prob = t.nn.functional.softmax(score, dim=1)[:1].data.tolist()

        total_img += 1
        if label.tolist()[0] == prob[0].index(max(prob[0])):
            correct_img += 1

        print('{}/{} {}  {}'.format(i+1, 
                                    num_val_data, 
                                    prob[0].index(max(prob[0])),
                                    prob))

accuracy = (correct_img/total_img)*100

print(' Avg_loss: {:.8f}\n'.format(float(avg_loss)),
      'Accuracy:({}/{}) {:.4f}% '.format(correct_img, total_img, accuracy),)

