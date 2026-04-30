# Kimi K2.6 Smoke Tests

Date: 2026-04-30

Task: `contacts.update_contact_phone`

## Stagehand

Command forced `BENCHMARK_MODEL=kimi-k2.6` through DashScope's OpenAI-compatible endpoint.

Result: did not run. Stagehand launched, then DashScope rejected the model on the first LLM request:

`InvalidParameter: Unsupported model: 'kimi-k2.6'`

Primary artifact: `stagehand_contacts_update_contact_phone_debug/`

## Magnitude

Command forced `BENCHMARK_PROVIDER=openai-generic` and `BENCHMARK_MODEL=kimi-k2.6`.

Result: ran with Kimi but timed out after 900s without completing the simple contact edit.

Wrapper stdout confirms:

`Magnitude: using openai-generic/kimi-k2.6`

Primary artifact: `magnitude_contacts_update_contact_phone/`
