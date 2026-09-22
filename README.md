# Open WebUI Reasoning Effort Filters

Per-chat reasoning effort controls for GPT-5.6 Sol/Terra/Luna and GPT-6 Astra.

## Filters

| File | Model IDs matched | Effort choices |
| --- | --- | --- |
| [reasoning_effort_gpt56.py](reasoning_effort_gpt56.py) | `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` | `default`, `none`, `low`, `medium`, `high`, `xhigh`, `max` |
| [reasoning_effort_astra.py](reasoning_effort_astra.py) | `gpt-6-astra` | `default`, `low`, `medium`, `high`, `xhigh`, `max` |

They have only been tested on **0.11.4**; other versions have not been tested but they probably work on the entire v0.11.x line. You have to use the Responses api. Chat Completions doesn't support reasoning effort.

## Why these exist

I wanted to choose reasoning effort from the chat instead of changing the model configuration each time, and have that choice sent in the format the connection expects.

Open WebUI users have reported that a configured `reasoning_effort` value can reach the Responses API unchanged, causing an HTTP 400 because that endpoint expects nested `reasoning.effort`. The history is documented in [#23566](https://github.com/open-webui/open-webui/issues/23566) and [#28418](https://github.com/open-webui/open-webui/issues/28418). [Discussion #28421](https://github.com/open-webui/open-webui/discussions/28421) proposes an upstream remap and discusses using nested custom parameters. These filters provide a convenient selectable control for my setup while that upstream behavior is being discussed.

The filters use the `request()` hook and read the connection's `api_type`, because the body is still Chat-Completions-shaped before Open WebUI converts it for Responses. An explicit selection sends nested `reasoning.effort` for Responses or flat `reasoning_effort` for Chat Completions, removing the incompatible parameter. Responses requests retain other fields in an existing `reasoning` object.

GPT-5.6 offers an explicit `none` option; Astra omits it and guards against stale saved `none` settings. `default` leaves the request unchanged—it does not remove reasoning settings already supplied elsewhere. Unrelated models are unchanged, and applying an explicit selection repeatedly during a tool loop has the same result.

The connection lookup depends on Open WebUI internals (`urlIdx` and `openai.api_configs`) and has only been tested here on **0.11.4**. If configuration cannot be read, the filters assume Chat Completions. An upstream remap could make the format workaround unnecessary; the selectable effort control would still be useful.

## Installation and use

1. In Open WebUI, open **Admin Panel → Functions → Import From Link**.
2. Paste the link for the desired filter:
   - [GPT-5.6 filter](https://github.com/firkin-gadabout/openwebui-reasoning-effort-filters/blob/main/reasoning_effort_gpt56.py)
   - [GPT-6 Astra filter](https://github.com/firkin-gadabout/openwebui-reasoning-effort-filters/blob/main/reasoning_effort_astra.py)
3. Review the code, save and enable the function, and attach it to the appropriate model. Set it as a Default Filter so it's on the prompt bar when those models are selected.
4. Set `effort` when sending your prompt or leave it default.

See the [Open WebUI Functions documentation](https://docs.openwebui.com/features/extensibility/plugin/functions/) for importing functions and configuring user valves.

## Source and license

I vibe-coded these filters with AI assistance for my own Open WebUI setup. I’m sharing that openly because I believe transparency is good community practice.

Licensed under the [MIT License](LICENSE).
