import time
import logging
import signal
import sys
from typing import Optional
from .config import config
from .gpio_driver import FanDriver
from .utils import read_cpu_temp_c

logger = logging.getLogger('misfans')


class FanController:
    def __init__(self):
        self.fan: FanDriver = FanDriver(config.FAN_PIN)
        self.on_temp: float = config.ON_TEMP
        self.off_temp: float = config.OFF_TEMP
        self.interval: float = config.POLL_INTERVAL
        self._running: bool = True

    def check_once(self) -> None:
        temp: Optional[float] = read_cpu_temp_c()
        if temp is None:
            logger.warning('Could not read temperature')
            return
        logger.debug('Current temp: %sC', temp)
        if not self.fan.is_active() and temp >= self.on_temp:
            logger.info(
                'Current temperature %sC above on threshold — starting fan',
                temp,
            )
            self.fan.on()
        elif self.fan.is_active() and temp <= self.off_temp:
            logger.info(
                'Current temperature %sC below off threshold — stopping fan',
                temp,
            )
            self.fan.off()

    def run(self) -> None:
        logger.info('Starting misfans daemon')
        while self._running:
            try:
                self.check_once()
            except Exception:
                logger.exception('Error in main loop')
            time.sleep(self.interval)

    def stop(self) -> None:
        logger.info('Stopping misfans daemon')
        self._running = False
        try:
            self.fan.off()
        except Exception:
            logger.exception('Error while stopping fan')


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    controller = FanController()

    def _handle(sig, frame):
        logger.info('Received signal %s, shutting down', sig)
        controller.stop()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _handle)
    signal.signal(signal.SIGINT, _handle)

    controller.run()


if __name__ == '__main__':
    main()
