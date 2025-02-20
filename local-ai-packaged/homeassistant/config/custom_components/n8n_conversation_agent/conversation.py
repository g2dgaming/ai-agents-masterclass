import requests
import logging
from homeassistant.components.conversation import ConversationEntity, ConversationInput, ConversationResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from .const import DEFAULT_WEBHOOK_URL

_LOGGER = logging.getLogger(__name__)

class N8NConversationEntity(ConversationEntity):
    """A conversation entity that forwards queries to an n8n webhook."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the n8n conversation entity."""
        self.hass = hass

    @property
    def supported_languages(self):
        """Return the list of supported languages."""
        return ["*"]  # Supports all languages

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Process a sentence and return a response from n8n."""
        _LOGGER.debug("Forwarding user input to n8n: %s", user_input.text)
        response = intent.IntentResponse(language=user_input.language)

        try:
            result = await self.hass.async_add_executor_job(
                self._send_to_n8n, user_input.text
            )
            response.async_set_speech(result)
        except Exception as e:
            _LOGGER.error("Error contacting n8n: %s", e)
            response.async_set_speech("I'm having trouble connecting to n8n right now.")

        return ConversationResult(
            response=response,
            conversation_id=user_input.conversation_id,
        )

    def _send_to_n8n(self, text: str) -> str:
        """Send a message to the n8n webhook and return the response."""
        try:
            response = requests.post(DEFAULT_WEBHOOK_URL, json={"message": text}, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response from n8n.")
        except Exception as e:
            return f"Error contacting n8n: {e}"
