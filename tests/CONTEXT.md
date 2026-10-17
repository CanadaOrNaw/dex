# Dex server checks: folder contract

Integration checks that expect the HTTP server, not a standalone proof of model quality.

## Entry routes

- [workspace contract](../CONTEXT.md).
- [server checks](test_server.py).
- [server source](../server/dex_server.py).
- [run instructions](../README.md).

## Inputs

An explicitly authorized running server and the test source; root README describes the expected setup.

## Process

Inspect the target before running test_server.py. Do not start a server, load model weights or contact an endpoint merely to validate document links.

## Outputs

A completed result tied to the checked server/code when tests actually run; filenames alone are not a passing receipt.

## Human check

Local API checks do not establish general accuracy, calibration or deployment safety. Report failures and untested paths honestly.
