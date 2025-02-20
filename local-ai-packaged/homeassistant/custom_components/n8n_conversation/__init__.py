"""Initialize the n8n Conversation Agent integration."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .conversation import N8NConversationAgent
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the n8n Conversation component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up n8n conversation agent from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    agent = N8NConversationAgent(hass, entry.data["webhook_url"])
    hass.data[DOMAIN][entry.entry_id] = agent

    hass.services.async_register(DOMAIN, "ask", agent.async_process)

    # Register as a Home Assistant Conversation Agent
    hass.components.conversation.async_set_agent(hass.data[DOMAIN][entry.entry_id])

    return True


async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    """Unload the integration."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
