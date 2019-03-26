#!/urs/bin/env python3

class DefaultConfig():
    
    use_gpu = True
    gpu_id = 0
    num_workers = 2

    input_size = 224

    # for training setting
    pretrained = False
    load_model = 'ResNet50-epoch199.pth'
    train_dir = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/train_all'
    train_batch_size = 64 
    base_lr = 0.001
    lr_decay_step =300 
    max_epoch = 800
    show_iter = 100 
    save_iter = 1000

    # for validation setting
    val = False
    val_dir   = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/val_data'
    val_iter = 500
    val_batch_size = 32

    # for testing setting
    test_model = 'ResNet50-epoch150.pth'
    test_dir  = '/mnt/sdc1/work/kaggle/Aerial_Cactus_Identification/test'
    title_output = 'id,has_cactus'

