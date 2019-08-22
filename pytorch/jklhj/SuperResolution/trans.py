#!/usr/bin/env python3

import torch as t
import torchvision as tv
from torchvision import transforms as T

from transformer_net import TransformerNet

@t.no_grad()
def stylize(DC):
    trans_gpu_id = DC.trans_gpu_id
    device = t.device('cuda', trans_gpu_id) if DC.use_gpu else t.device('cpu')

    # Image preprocessing
    content_img = tv.datasets.folder.default_loader(DC.low_resol_img)
    content_transform = T.Compose([
      T.ToTensor(),
      T.Lambda(lambda x: x.mul(255))
    ])

    content_img = content_transform(content_img)
    content_img = content_img.unsqueeze(0).to(device).detach()

    # Load model
    trans_model = TransformerNet().eval()
    trans_model.load_state_dict(t.load(DC.trans_model, 
                                       map_location=lambda storage, 
                                       loc: storage))

    trans_model.to(device)

    # Save the transformer image
    output = trans_model(content_img)
    output_data = output.cpu().data[0]
    tv.utils.save_image( (output_data/255).clamp(min=0, max=1), DC.result_img )

if __name__ == '__main__':
    from config import DefaultConfig as DC

    stylize(DC)
