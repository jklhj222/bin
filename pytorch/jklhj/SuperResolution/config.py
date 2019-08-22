#!/usr/bin/env python3

class DefaultConfig():

    use_gpu = True
    num_workers = 2
    input_size = 288

    # for training setting
    train_gpu_id = 0
    train_batch_size = 4

    load_model = ''

    HighResol_dir = '/home/hugh/tmp/train2014_10k'
    LowResol_dir =  '/home/hugh/tmp/train2014_GaussianBlur_10k'

    super_resol_factor = 4

    base_lr = 1e-3

    content_weight = 1

    max_epoch = 80

    show_iter = 50
    save_iter = 200

    # for transforming setting
    trans_gpu_id = 0
    trans_model = '79_style.pth'
    low_resol_img = 'train_49987.png'

    result_img = 'result.jpg'

    
