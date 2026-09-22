# Open WebUI Reasoning Effort Filters

Per-chat reasoning effort controls for GPT-5.6 Sol/Terra/Luna and GPT-6 Astra, with connection-aware handling for Chat Completions and Responses API requests.

## Filters

| File | Model IDs matched | Effort choices |
| --- | --- | --- |
| [reasoning_effort_gpt56.py](reasoning_effort_gpt56.py) | `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` | `default`, `none`, `low`, `medium`, `high`, `xhigh`, `max` |
| [reasoning_effort_astra.py](reasoning_effort_astra.py) | `gpt-6-astra` | `default`, `low`, `medium`, `high`, `xhigh`, `max` |

Both filters retain version **1.3.0** and declare **Open WebUI 0.11.4** as their minimum requirement. They have only been tested on **0.11.4**; other versions have not been tested. Use an OpenAI-compatible connection configured for the corresponding models.

## Why these exist

The filters use the connection's `api_type` setting instead of guessing the API from the request body. For an explicit effort selection, they send nested `reasoning.effort` for Responses connections or flat `reasoning_effort` for Chat Completions, removing the incompatible parameter.

`default` leaves the request unchanged, including any reasoning settings already present. Requests for unrelated models are also unchanged. If connection configuration cannot be read, the filters fall back to Chat Completions. Astra omits `none` and includes a guard for stale saved settings containing it.

## Installation and use

1. In Open WebUI, open **Admin Panel → Functions → Import From Link**.
2. Paste the link for the desired filter:
   - [GPT-5.6 filter](https://github.com/firkin-gadabout/openwebui-reasoning-effort-filters/blob/main/reasoning_effort_gpt56.py)
   - [GPT-6 Astra filter](https://github.com/firkin-gadabout/openwebui-reasoning-effort-filters/blob/main/reasoning_effort_astra.py)
3. Review the code, save and enable the function, and attach it to the appropriate model.
4. Select the filter in the chat and set `effort` in its user valves.

See the [Open WebUI Functions documentation](https://docs.openwebui.com/features/extensibility/plugin/functions/) for importing functions and configuring user valves.

## Source and license

I vibe-coded these filters with AI assistance for my own Open WebUI setup. I’m sharing that openly because I believe transparency is good community practice.

The Python files preserve the original filters’ working logic, with the declared Open WebUI requirement updated to 0.11.4. Export wrapper metadata is excluded.

Licensed under the [MIT License](LICENSE).
