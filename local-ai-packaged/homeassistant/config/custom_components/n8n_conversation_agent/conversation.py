import logging
import requests
from homeassistant.components.conversation import (
    ConversationEntity,
    ConversationInput,
    ConversationResult,
)
from homeassistant.core import HomeAssistant
from .const import WEBHOOK_URL

_LOGGER = logging.getLogger(__name__)

class N8NConversationAgent(ConversationEntity):
    """A conversation agent that forwards all queries to an n8n webhook."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the n8n agent."""
        self.hass = hass

    @property
    def attribution(self):
        """Return the attribution for this agent."""
        return {"name": "n8n Conversation Agent", "url": "https://n8n.io/"}

    @property
    def supported_languages(self):
        """Return the list of supported languages."""
        return ["en", "es", "fr", "de", "it", "hi", "zh", "ar"]  # Add more if needed

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Process a query and return a response from n8n."""
        _LOGGER.debug("Forwarding query to n8n: %s", user_input.text)

        try:
            response_text = await self.hass.async_add_executor_job(
                self._send_to_n8n, user_input.text
            )
        except Exception as e:
            _LOGGER.error("Error contacting n8n: %s", e)
            response_text = "I'm having trouble connecting to n8n right now."

        return ConversationResult(response_text)

    def _send_to_n8n(self, query: str) -> str:
        """Send a message to n8n and return the response."""
        try:
            response = requests.post(
                WEBHOOK_URL, json={"message": query}, timeout=10
            )
            response.raise_for_status()
            return response.json().get("response", "No response from n8n.")
        except Exception as e:
            _LOGGER.error("Error sending request to n8n: %s", e)
            return f"Error: {e}"
