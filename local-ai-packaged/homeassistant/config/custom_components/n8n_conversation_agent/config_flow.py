import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN

class N8NConversationAgentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for N8N Conversation Agent."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            webhook_url = user_input.get("webhook_url")
            title=user_input.get("title")
            if self._is_valid_url(webhook_url):
                return self.async_create_entry(
                    title=title,
                    data={"webhook_url": webhook_url},
                )
            else:
                errors["webhook_url"] = "invalid_url"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("webhook_url"): str,
                    vol.Required("title"): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Validate the provided URL."""
        from urllib.parse import urlparse

        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
