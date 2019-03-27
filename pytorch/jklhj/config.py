#!/urs/bin/env python3

class DefaultConfig():
    
    use_gpu = True
    num_workers = 2

    input_size = 512

    # for training setting
    train_gpu_id = 1
    pretrained = False
    load_model = ''
    train_dir = '/home/hugh/Dropbox/tmp-PC/pytorch/train_data'
#    train_dir = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/train_data'
    train_batch_size = 12
    base_lr = 0.001
    lr_decay_step =150 
    max_epoch = 500
    show_iter = 50 
    save_iter = 5000

    # for validation setting
    val = True
    val_dir   = '/home/hugh/Dropbox/tmp-PC/pytorch/val_data'
#    val_dir   = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/val_data'
    val_iter = 500
    val_batch_size = 1

    # for testing setting
    test_gpu_id = 0
    test_model = 'ResNet101-iter3297.pth'
    test_dir  = '/home/hugh/Dropbox/tmp-PC/pytorch/test'
    title_output = 'id,has_cactus'

