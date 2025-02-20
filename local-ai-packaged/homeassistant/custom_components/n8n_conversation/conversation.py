"""n8n Conversation Agent for Home Assistant."""
import requests
import logging
from homeassistant.components.conversation import ConversationAgent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

_LOGGER = logging.getLogger(__name__)

class N8NConversationAgent(ConversationAgent):
    """A conversation agent that uses an n8n webhook."""

    def __init__(self, hass: HomeAssistantType, webhook_url: str):
        """Initialize the agent."""
        self.hass = hass
        self.webhook_url = webhook_url

    @property
    def attribution(self):
        """Return attribution."""
        return "Powered by n8n"

    @property
    def name(self):
        """Return the name of the agent."""
        return "n8n Conversational Agent"

    async def async_process(self, user_input: str):
        """Process a sentence and return a response using the n8n webhook."""
        _LOGGER.debug("Sending user input to n8n: %s", user_input)

        try:
            response = await self.hass.async_add_executor_job(
                self._send_to_n8n, user_input
            )
            _LOGGER.debug("n8n Response: %s", response)
            return response
        except Exception as e:
            _LOGGER.error("Error contacting n8n: %s", e)
            return "I'm having trouble connecting to my brain right now."

    def _send_to_n8n(self, text: str) -> str:
        """Send a message to the n8n webhook and return the response."""
        try:
            response = requests.post(self.webhook_url, json={"message": text}, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "response" in data:
                return data["response"]
            elif isinstance(data, dict) and "choices" in data:
                return data["choices"][0].get("text", "No response")
            else:
                return "Unexpected response format"
        except Exception as e:
            return f"Error contacting agent: {e}"
