import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .conversation import N8NConversationAgent

_LOGGER = logging.getLogger(__name__)

DOMAIN = "n8n_conversation_agent"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the n8n conversation agent from configuration.yaml."""
    if DOMAIN not in config:
        return True

    _LOGGER.info("Setting up n8n conversation agent from configuration.yaml")

    agent = N8NConversationAgent(hass)
    hass.data[DOMAIN] = agent

    # Register the agent with Home Assistant's conversation component
    hass.components.conversation.async_set_agent(hass, agent)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up N8N Conversation Agent from a config entry."""
    agent = N8NConversationAgent(hass)
    hass.data[entry.entry_id] = agent

    # Register the agent with Home Assistant's conversation component
    hass.components.conversation.async_set_agent(entry, agent)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unregister the agent
    hass.components.conversation.async_unset_agent(entry)

    # Clean up
    hass.data.pop(entry.entry_id)

    return True
