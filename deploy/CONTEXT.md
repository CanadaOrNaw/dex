# Dex deployment definitions: folder contract

Keep the systemd definition distinct from live service state.

## Entry routes

- [workspace contract](../CONTEXT.md).
- [service definition](dex.service).
- [container definition](../Dockerfile).
- [use guide](../README.md).

## Inputs

The explicit deployment request, target machine details, existing service/container definitions and selected model path.

## Process

Review paths, dependencies, binding and authentication for the target before deployment. A checked-in service definition is not installed/running-service evidence.

## Outputs

Deployment definitions in this repo. Installed units, containers and models remain runtime state outside the documentation contract.

## Human check

Zack approves installation, activation, restart and publication. This ICM pass neither runs the service nor changes runtime configuration.
