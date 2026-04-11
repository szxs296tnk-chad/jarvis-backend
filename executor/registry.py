from __future__ import annotations

import logging

from adapters.pc.pc_adapter import (
    open_youtube,
    open_netflix,
    open_browser,
    open_spotify,
    open_notes,
    open_calculator,
    screenshot,
    shutdown,
    restart,
    set_volume,
)
from adapters.web.web_adapter import (
    search_google,
    get_request,
    post_request,
    trigger_n8n,
)
from adapters.home.home_adapter import (
    turn_on_light,
    turn_off_light,
    set_temperature,
    get_sensor_state,
)

logger = logging.getLogger("chad.executor.registry")

TOOLS: dict[str, callable] = {
    "OPEN_YOUTUBE":     open_youtube,
    "OPEN_NETFLIX":     open_netflix,
    "OPEN_BROWSER":     open_browser,
    "OPEN_SPOTIFY":     open_spotify,
    "OPEN_NOTES":       open_notes,
    "OPEN_CALCULATOR":  open_calculator,
    "SCREENSHOT":       screenshot,
    "SHUTDOWN_PC":      shutdown,
    "RESTART_PC":       restart,
    "SET_VOLUME":       set_volume,
    "SEARCH_GOOGLE":    search_google,
    "HTTP_GET":         get_request,
    "HTTP_POST":        post_request,
    "N8N_TRIGGER":      trigger_n8n,
    "TURN_ON_LIGHT":    turn_on_light,
    "TURN_OFF_LIGHT":   turn_off_light,
    "SET_TEMPERATURE":  set_temperature,
    "GET_SENSOR":       get_sensor_state,
}
