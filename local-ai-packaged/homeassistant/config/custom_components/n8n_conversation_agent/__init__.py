import logging
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the n8n conversation agent."""
    _LOGGER.info("Setting up n8n Conversation Agent")
    return True
