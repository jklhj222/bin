#!/usr/bin/env python3

class DefaultConfig():

    use_gpu = True
    num_workers = 2
    
    input_size = 96 

    # for training setting
    train_gpu_id = 0

    train_netd_model = ''
    train_netg_model = ''

    train_dir = './data'
    train_batch_size = 256
    base_lrg = 2e-4
    base_lrd = 2e-4

    lr_decay_step = 100

    g_train_every = 5
    d_train_every = 1

    max_epoch = 200

    adam_beta1 = 0.5

    nz = 100
    ngf = 64
    ndf = 64

    show_iter = 50
    save_iter = 600
    pic_save_dir = './imgs'

    # for testing setting
    test_img = 'result.png'
    test_netg_model = ''
    test_netd_model = ''

    #  pick 64 best pictures of 512 generated pictures
    gen_num = 64
    gen_search_num = 512
    gen_mean = 0
    gen_std = 1
