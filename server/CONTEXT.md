# Dex HTTP adapter: folder contract

The HTTP interface around the local typed-decision runtime.

## Entry routes

- [workspace contract](../CONTEXT.md).
- [server source](dex_server.py).
- [API/use guide](../README.md).
- [server checks](../tests/CONTEXT.md).

## Inputs

API request data and the selected local model at runtime; maintenance reads server source, requirements and documented request/response limits.

## Process

Keep HTTP validation/serialization changes scoped to this adapter. Resolve the root model-identity documentation conflict before asserting what weights are loaded.

## Outputs

HTTP responses and runtime diagnostics when explicitly launched; source edits otherwise. No running endpoint is certified here.

## Human check

Starting a model/server and exercising a live endpoint are separate authorized runtime actions. Do not leak tokens, infer correctness from typed output, or change deployment during a docs check.
