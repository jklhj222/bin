#!/usr/bin/env python3

class DefaultConfig():

    use_gpu = True
    num_workers = 2

    input_size = 256

    # for training setting
    train_gpu_id = 1

    load_model = ''

    train_content_dir = '/mnt/sda1/jklhj/coco'
    style_img = 'style.jpg'

    train_batch_size = 8
    base_lr = 1e-3

    content_weight = 1e5
    style_weight = 1e10

    max_epoch = 2

    show_iter = 50
    save_iter = 200

    # for transforming setting
    trans_gpu_id = 0
#    style_model = 'checkpoints_relu2_2/1_style.pth'
    style_model = '0_style.pth'
    content_img = 'amber.jpg'
    result_img = 'amber_relu2_2_new2.jpg'

    
