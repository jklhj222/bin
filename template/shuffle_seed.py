#!/usr/bin/env python3

import random

randnum = random.randint(0,100)
random.seed(randnum)
random.shuffle(train_x)
random.seed(randnum)
random.shuffle(train_y)
