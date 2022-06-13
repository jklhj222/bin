#!/usr/bin/env python3
import time

class TimePeriod():
    def __init__(self, skip_steps=20, start_t=time.time()):
        import time

        self.start_t = start_t

        self.last_t = start_t

        self.skip_steps = skip_steps

        self.call_times = 0

        self.total_t = 0

    def accumulate(self, period_t):
        self.call_times += 1

        if self.call_times > self.skip_steps:
            self.total_t += period_t

    def calc_period(self):
        period_t = time.time() - self.last_t

        period_fps = 1 / period_t

        self.accumulate(period_t)

        self.last_t = time.time()

        if self.total_t != 0:
            total_fps = (self.call_times - self.skip_steps) / self.total_t

        else:
            total_fps = 0 

        return self.call_times, period_t, period_fps, self.total_t, total_fps


if __name__ == '__main__':
    time_period = TimePeriod()

    while True:
        t = time_period.calc_period()

        time.sleep(1)

        print(t)   





