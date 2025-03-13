"""The n8n Conversation Agent integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up n8n Conversation Agent from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "conversation")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if await hass.config_entries.async_forward_entry_unload(entry, "conversation"):
        hass.data[DOMAIN].pop(entry.entry_id, None)
        return True
    return False
