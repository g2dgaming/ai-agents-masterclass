from homeassistant import config_entries
from .const import DOMAIN  # Ensure DOMAIN is defined in your const.py

class N8NConversationAgentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for N8N Conversation Agent."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Process user input and create the config entry
            return self.async_create_entry(title="N8N Conversation Agent", data=user_input)

        # Show the configuration form to the user
        return self.async_show_form(step_id="user")
