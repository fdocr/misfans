import time
import logging
from .config import config
from .gpio_driver import FanDriver
from .utils import read_cpu_temp_c

logger = logging.getLogger('misfans')


class FanController:
    def __init__(self):
        self.fan = FanDriver(config.FAN_PIN)
        self.on_temp = config.ON_TEMP
        self.off_temp = config.OFF_TEMP
        self.interval = config.POLL_INTERVAL
        self.last_state = False

    def check_once(self):
        temp = read_cpu_temp_c()
        if temp is None:
            logger.warning('Could not read temperature')
            return
        logger.debug(f'Current temp: {temp}C')
        if not self.fan.is_active() and temp >= self.on_temp:
            logger.info('Temperature above on threshold — starting fan')
            self.fan.on()
            self.last_state = True
        elif self.fan.is_active() and temp <= self.off_temp:
            logger.info('Temperature below off threshold — stopping fan')
            self.fan.off()
            self.last_state = False

    def run(self):
        logger.info('Starting misfans daemon')
        while True:
            try:
                self.check_once()
            except Exception as e:
                logger.exception('Error in main loop')
            time.sleep(self.interval)


def main():
    logging.basicConfig(level=logging.INFO)
    c = FanController()
    c.run()


if __name__ == '__main__':
    main()
