#!/usr/bin/env python3

import torch as t
import torchvision as tv

from config import DefaultConfig as DC
import model

@t.no_grad()
def generate(config):
    device = t.device('cuda') if config.use_gpu else t.device('cpu')

    netg = model.NetG(config).eval()
    netd = model.NetD(config).eval()

    noises = t.randn(config.gen_search_num, config.nz, 1, 1)
    noises = noises.normal_(config.gen_mean, config.gen_std).to(device)

    netg.load_state_dict(t.load(config.test_netg_model, 
                                map_location=lambda storage, loc: storage))
    netd.load_state_dict(t.load(config.test_netd_model, 
                                map_location=lambda storage, loc: storage))

    netg.to(device)
    netd.to(device)

    # generate the pictures from NetD, and calculate the scores 
    fake_img = netg(noises)
    scores = netd(fake_img).detach()

    # pick the best gen_num pictures
    indices = scores.topk(config.gen_num)[1]

    result = []

    for i in indices:
        result.append(fake_img.data[i])

    tv.utils.save_image(t.stack(result), 
                        config.test_img, 
                        normalize=True, 
                        range=(-1, 1))

if __name__ == '__main__':
    from config import DefaultConfig as DC

    generate(DC)
