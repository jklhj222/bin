#!/bin/bash
## 0. Import web service and darknet docker images
##    docker load -i adatapi_hugh_20181107.tar 
##    docker load -i adatdarknet_v2.4_hugh_20181107.tar

## 1. start the web service container
ADATAPI_CONTAINER_NAME='adatapi_hugh'

docker create -it --name "$ADATAPI_CONTAINER_NAME" -p 8080:8080 adatapi_hugh_20181107 /bin/bash

docker start "$ADATAPI_CONTAINER_NAME"
docker exec -d "$ADATAPI_CONTAINER_NAME" /bin/bash -c "./root/adatapi.sh start"

sleep 5

## 2. start the darknet container 
data_path='data/'
example_path='test.MTS'
#cfg_dir_path='/mnt/sda1/work/MIC_X3_plug/docker_script_adat20180720/update20180720/weight_micplug03/'
cfg_dir_path='/mnt/sda1/work/Aviation/Aviation_20180820/AACL_AI_Training_material_20180820_training/yolo_train_down/cfg/'
#CFG_NAME='micplug03.cfg'
CFG_NAME='adat00_inference.cfg'
CFG_DATA_NAME='adat.data'
#weights_dir_path='/mnt/sda1/work/MIC_X3_plug/docker_script_adat20180720/update20180720/weight_micplug03/'
weights_dir_path='/mnt/sda1/work/Aviation/Aviation_20180820/AACL_AI_Training_material_20180820_training/yolo_train_down/backup'
#WEIGHT_NAME='micplug03_final.weights'
WEIGHT_NAME='adat00_10000.weights'
DARKNET_CONTAINER_NAME='adatdarknet_hugh'

THRESH=0.1

# transfer the directories to absolute path
DATA_PATH=`realpath "$data_path"`
EXAMPLE_PATH=`realpath "$example_path"`
CFG_DIR_PATH=`realpath "$cfg_dir_path"`
WEIGHTS_DIR_PATH=`realpath "$weights_dir_path"`

mkdir -p "$DATA_PATH"/images
chmod 777 -R "$DATA_PATH"

find "$DATA_PATH"/images/ -name *.jpg | xargs rm
rm -f "$DATA_PATH"/*.txt

## 3. execute darknet yolo detection
#nvidia-docker create --name "$DARKNET_CONTAINER_NAME" -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v "$CFG_DIR_PATH":/root/darknet_v2.4/adat_cfg -v "$WEIGHTS_DIR_PATH":/root/darknet_v2.4/adat_weights --mount type=bind,source="$DATA_PATH",target=/data/ --mount type=bind,source="$UPDATE_PATH",target=/root/update/ -it adatdarknet_v2.4 /bin/bash
nvidia-docker create --name "$DARKNET_CONTAINER_NAME" -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v "$CFG_DIR_PATH":/root/darknet_v2.4/adat_cfg -v "$WEIGHTS_DIR_PATH":/root/darknet_v2.4/adat_weights --mount type=bind,source="$DATA_PATH",target=/data/ -it adatdarknet_v2.4_hugh_20181107 /bin/bash

nvidia-docker start "$DARKNET_CONTAINER_NAME"

echo '#!/bin/bash' > darknet_exec.sh
echo 'cd /root/darknet_v2.4' >> darknet_exec.sh
echo './darknet detector demo2 /root/darknet_v2.4/adat_cfg/'"$CFG_DATA_NAME" '/root/darknet_v2.4/adat_cfg/'"$CFG_NAME" '/root/darknet_v2.4/adat_weights/'"$WEIGHT_NAME" '/data/images/ -prefix /data/res -avg 1 -thresh '"$THRESH" >> darknet_exec.sh

docker cp darknet_exec.sh "$DARKNET_CONTAINER_NAME":/root/darknet_v2.4/

nvidia-docker exec -it "$DARKNET_CONTAINER_NAME" /bin/bash -c 'bash /root/darknet_v2.4/darknet_exec.sh'
