import numpy as np

from saleae.range_measurements import DigitalMeasurer

class BaudRateEstimate(DigitalMeasurer):
    supported_measurements = ["baud_rate"]

    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)
        self.pulses = []
        self.state = None
        self.last_edge = None

    def process_data(self, data):
        for time, bitstate in data:
            if self.state is not None and self.last_edge is not None and self.state != bitstate:
                self.pulses.append(float(time - self.last_edge))
            self.last_edge = time
            self.state = bitstate

    def measure(self):
        return { "baud_rate": 1 / np.percentile(self.pulses, 1) }
