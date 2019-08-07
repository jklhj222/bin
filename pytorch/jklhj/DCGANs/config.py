#!/usr/bin/env python3

class DefaultConfig():

    use_gpu = True
    num_workers = 2
    
    input_size = 100

    # for training setting
    train_gpu_id = 0

    load_netd_model = ''
    load_netg_model = ''

    train_dir = './data'
    train_batch_size = 768
    base_lrg = 0.001
    base_lrd = 0.001

    lr_decay_step = 100

    g_train_every = 1
    d_train_every = 5

    max_epoch = 200

    adam_beta1 = 0.5

    nz = 100
    ngf = 64
    ndf = 64

    show_iter = 50
    save_iter = 200
    pic_save_dir = './imgs'

    # for testing setting
    test_img = 'result.png'

    #  pick 64 best pictures of 512 generated pictures
    gen_num = 64
    gen_search_num = 512
    gen_mean = 0
    gen_std = 1
