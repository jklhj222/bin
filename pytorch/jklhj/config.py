#!/urs/bin/env python3

class DefaultConfig():
    pretrained = False
    load_model = 'ResNet50-epoch199.pth'
    
    use_gpu = True
    gpu_id = 0
    num_workers = 2

    input_size = 512

    # for training setting
    train_dir = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/train_data'
    train_batch_size = 512
    base_lr = 0.001
    lr_decay_step =350 
    max_epoch = 1000
    show_iter = 100 
    save_iter = 1000

    # for validation setting
    val = True
    val_dir   = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/val_data'
    val_iter = 500
    val_batch_size = 32

    # for testing setting
    test_model = 'ResNet50-epoch150.pth'
    test_dir  = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/test'
    title_output = 'id,has_cactus'

