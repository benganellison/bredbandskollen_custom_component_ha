import asyncio

import logging

import voluptuous as vol

from datetime import timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

from homeassistant.util import Throttle

CONF_PATH = 'path'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PATH): cv.string
})

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'bredbandskollen'

SCAN_INTERVAL = timedelta(minutes=10)

MAPPING = {
    'latency': 3,
    'download': 1,
    'upload': 2
}


class Bredbandskollen:

    def __init__(self, cmd):
        self.data = []
        self._cmd = cmd
        self.is_polling = False

    async def async_update(self):
        if not self.is_polling:
            self.is_polling = True
            data = await run(self._cmd + ' --duration=6 --quiet')
            self.data = data.split(' ')
            self.is_polling = False


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        return stdout.decode()
    else:
        _LOGGER.error("{} {}".format(proc.returncode, stderr.decode()))


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):
    """Set up the platform."""
    data = Bredbandskollen(config[CONF_PATH])
    await data.async_update()
    entities = [
        Sensor('latency', data),
        Sensor('upload', data),
        Sensor('download', data)
    ]
    async_add_entities(entities)


class Sensor(Entity):
    """Representation of a sensor."""

    def __init__(self, sensor_unit=None, data=None):
        """Init the sensor."""
        self._type = sensor_unit
        self.data = data
        self._state = data.data[MAPPING[self._type]]
        self._name = 'Bredbandskollen {}'.format(sensor_unit)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._type == 'latency':
            return "ms"
        return "Mbit/s"

    @property
    def state(self):
        """Property for the state attributes."""
        return self._state

    @property
    def name(self):
        """Name property for sensor."""
        return self._name

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self.data.async_update()
        try:
            self._state = self.data.data[MAPPING[self._type]]
        except IndexError:
            self._state = None