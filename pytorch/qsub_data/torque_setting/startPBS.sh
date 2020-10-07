#!/bin/bash

/etc/init.d/torque-server restart
/etc/init.d/torque-scheduler restart
/etc/init.d/torque-mom restart
sudo qterm

sudo pbs_server
sudo pbs_sched
sudo pbs_mom
