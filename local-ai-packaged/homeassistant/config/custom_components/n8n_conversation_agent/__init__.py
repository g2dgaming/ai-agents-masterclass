from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.components import conversation
from .conversation import N8NConversationEntity
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the n8n Conversation component."""
    entity = N8NConversationEntity(hass)
    hass.data[DOMAIN] = entity
    conversation.async_set_agent(hass, entity)
    return True
