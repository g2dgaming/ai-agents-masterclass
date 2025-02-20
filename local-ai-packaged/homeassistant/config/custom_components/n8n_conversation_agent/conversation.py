from __future__ import annotations

import json
import logging
import requests
from typing import Any, Literal

from homeassistant.components import assist_pipeline, conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MATCH_ALL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import intent
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up conversation entities."""
    agent = N8NConversationEntity(config_entry)
    async_add_entities([agent])


class N8NConversationEntity(
    conversation.ConversationEntity
):
    """n8n conversation agent."""

    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.entry = entry
        self._attr_name = entry.title
        self._attr_unique_id = entry.entry_id

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        await super().async_added_to_hass()
        assist_pipeline.async_migrate_engine(
            self.hass, "conversation", self.entry.entry_id, self.entity_id
        )
        conversation.async_set_agent(self.hass, self.entry, self)
        self.entry.async_on_unload(
            self.entry.add_update_listener(self._async_entry_update_listener)
        )

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from Home Assistant."""
        conversation.async_unset_agent(self.hass, self.entry)
        await super().async_will_remove_from_hass()

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence."""
        return await self._async_handle_message(user_input)

    async def _async_handle_message(
        self,
        user_input: conversation.ConversationInput,
    ) -> conversation.ConversationResult:
        """Call the n8n webhook API."""
        webhook_url = self.entry.data.get("webhook_url")
        if not webhook_url:
            raise HomeAssistantError("No n8n webhook URL configured.")

        try:
            response = await self.hass.async_add_executor_job(self._send_to_n8n, webhook_url, user_input.text)
        except Exception as err:
            _LOGGER.error("Error communicating with n8n: %s", err)
            return conversation.ConversationResult(
                response=intent.IntentResponse(language=user_input.language, speech="Error contacting n8n."),
                conversation_id=user_input.conversation_id,
            )

        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(response)
        return conversation.ConversationResult(
            response=intent_response, conversation_id=user_input.conversation_id
        )

    def _send_to_n8n(self, webhook_url: str, query: str) -> str:
        """Send user query to n8n webhook and return response."""
        try:
            response = requests.post(
                webhook_url, json={"message": query}, timeout=10
            )
            response.raise_for_status()
            return response.json().get("response", "No response from n8n.")
        except requests.RequestException as err:
            _LOGGER.error("Request to n8n failed: %s", err)
            return "Error communicating with n8n."

    async def _async_entry_update_listener(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> None:
        """Handle options update."""
        await hass.config_entries.async_reload(entry.entry_id)
