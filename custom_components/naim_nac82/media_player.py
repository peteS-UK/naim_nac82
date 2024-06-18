from __future__ import annotations

import logging

from .const import DOMAIN

import voluptuous as vol

from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)

from homeassistant import config_entries, core

from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import (
    config_validation as cv,
    discovery_flow,
    entity_platform,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.start import async_at_start

_LOGGER = logging.getLogger(__name__)


from .const import (
    SERVICE_SEND_COMMAND,
    DEFAULT_NAME,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME, default=None): cv.string,
    }
)

SUPPORT_NAC82 = (
    MediaPlayerEntityFeature.VOLUME_STEP | MediaPlayerEntityFeature.VOLUME_MUTE
)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:

    config = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([NAC82Device(hass, config[CONF_NAME])])


class NAC82Device(MediaPlayerEntity):
    # Representation of a Emotiva Processor

    def __init__(self, hass, name):

        self._hass = hass
        self._entity_id = "media_player.naim_nac82"
        self._unique_id = "naim_nac82_" + name.replace(" ", "_").replace(
            "-", "_"
        ).replace(":", "_")
        self._device_class = "receiver"
        self._name = name
        self._muted = False

    should_poll = False

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return "mdi:audio-video"

    @property
    def state(self) -> MediaPlayerState:
        return MediaPlayerState.ON

    @property
    def name(self):
        # return self._device.name
        return None

    @property
    def has_entity_name(self):
        return True

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._unique_id)
            },
            name=self._name,
            manufacturer="Naim",
            model="NAC 82",
        )

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def device_class(self):
        return self._device_class

    @entity_id.setter
    def entity_id(self, entity_id):
        self._entity_id = entity_id

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        return SUPPORT_NAC82

    @property
    def is_volume_muted(self):
        return self._muted

    async def async_mute_volume(self, mute: bool) -> None:
        await self._hass.services.async_call(
            "remote",
            "send_command",
            {
                "entity_id": "remote.rm_mini_3",
                "num_repeats": "1",
                "delay_secs": "0.4",
                "device": "NAC 82",
                "command": "mute",
            },
        )
        self._muted = not self._muted
        self.async_schedule_update_ha_state()

    async def async_volume_up(self):
        await self._hass.services.async_call(
            "remote",
            "send_command",
            {
                "entity_id": "remote.rm_mini_3",
                "num_repeats": "1",
                "delay_secs": "0.4",
                "device": "NAC 82",
                "command": "volume_up",
            },
        )

    async def async_volume_down(self):
        await self._hass.services.async_call(
            "remote",
            "send_command",
            {
                "entity_id": "remote.rm_mini_3",
                "num_repeats": "1",
                "delay_secs": "0.4",
                "device": "NAC 82",
                "command": "volume_down",
            },
        )

    async def async_update(self):
        pass
