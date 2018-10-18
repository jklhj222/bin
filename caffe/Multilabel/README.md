#### Multilabel image classification with Caffe

1. Put multilabel_datalayers.py to $CAFFE_ROOT/examples/pycaffe/layers/

2. Build train and val model file, then replace the data layer with:
   type: "Python"
   module: "multilabel_datalayers"
   layer: "MultilabelDataLayerSync"
   
   and param_str,  
   see the exmaple files: trainnet_example.prototxt and valnet_example.prototxt .

3. Make the directory "images" which contains all the images for training and validation.

3. Build the train and val data set list with *.csv format,
   each line records the "image_file_path_without_extension","index of labels in each image, split with space"
   see the example files: train.csv and val.csv

4. Set the environment path in caffe_train.py
   execute caffe_train.py: 
                          python3 caffe_train.py 2> log
