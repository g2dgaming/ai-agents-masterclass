import logging
import requests
from homeassistant.components.assist_pipeline import (
    AssistPipelineAgent,
    PipelineResponse,
)
from homeassistant.core import HomeAssistant
from .const import WEBHOOK_URL, DOMAIN, AGENT_ID

_LOGGER = logging.getLogger(__name__)

async def async_get_agent(hass: HomeAssistant) -> "N8NAssistAgent":
    """Register the n8n agent for Assist Pipeline."""
    return N8NAssistAgent(hass)

class N8NAssistAgent(AssistPipelineAgent):
    """A conversation agent that forwards queries to an n8n webhook."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the n8n Assist Pipeline agent."""
        self.hass = hass

    @property
    def attribution(self):
        """Return attribution information."""
        return "Powered by n8n"

    @property
    def supported_languages(self):
        """Return the list of supported languages."""
        return ["*"]

    @property
    def id(self) -> str:
        """Return the unique agent ID for Assist Pipeline."""
        return AGENT_ID

    async def async_process(self, text: str, language: str) -> PipelineResponse:
        """Process a user query and return a response from n8n."""
        _LOGGER.debug("Forwarding user input to n8n: %s", text)

        try:
            result = await self.hass.async_add_executor_job(self._send_to_n8n, text)
            return PipelineResponse(text=result)
        except Exception as e:
            _LOGGER.error("Error contacting n8n: %s", e)
            return PipelineResponse(text="I'm having trouble connecting to n8n.")

    def _send_to_n8n(self, text: str) -> str:
        """Send a message to the n8n webhook and return the response."""
        try:
            response = requests.post(WEBHOOK_URL, json={"message": text}, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response from n8n.")
        except Exception as e:
            return f"Error contacting n8n: {e}"
