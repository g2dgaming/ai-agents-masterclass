"""Config flow for the n8n Conversation Agent integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_WEBHOOK_URL

_LOGGER = logging.getLogger(__name__)

class N8NConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for n8n Conversation Agent."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="n8n Conversation Agent", data=user_input)

        data_schema = vol.Schema({
            vol.Required("webhook_url", default=DEFAULT_WEBHOOK_URL): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return N8NOptionsFlowHandler(config_entry)

class N8NOptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow handler for n8n Conversation Agent."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required("webhook_url", default=self.config_entry.options.get("webhook_url", DEFAULT_WEBHOOK_URL)): str,
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
