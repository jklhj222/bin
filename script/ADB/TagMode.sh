#!/bin/bash

read -p 'Trun on or off the tag mode (on/off): ' onoff
echo turn $onoff tag mode.

if [ "$onoff" == "on" ]
then
  sudo docker cp lim:/var/www/config/Darknet_Func.json ./
  sed -i 's/\"show_bbox.*$/\"show_bbox\": \"True\",/g' Darknet_Func.json
  sudo docker cp ./Darknet_Func.json lim:/var/www/config/Darknet_Func.json
elif [ "$onoff" == "off" ]
then
  sudo docker cp lim:/var/www/config/Darknet_Func.json ./
  sed -i 's/\"show_bbox.*$/\"show_bbox\": \"False\",/g' Darknet_Func.json
  sudo docker cp ./Darknet_Func.json lim:/var/www/config/Darknet_Func.json
else
  echo 'please enter "on" or "off"'
fi

rm Darknet_Func.json
