## PowerPoint/Theory

1. Walk through the PowerPoint
2. Walk through the Scalers list: https://keda.sh/docs/2.16/scalers/?

## The App

1. Connect to ACR
2. Deploy the app within **app-deployment**
3. Confirm the app is running

## Installation

1. Walk through Helm Installation
2. Show the installation with a new cluster
3. Show the installation with an existing cluster

## Azure Portal

1. Go to the Azure portal
2. Walk through the steps in the `instructions.md` via the **KEDA** directory

## Manifest

1. Delete the existing cron job via the Azure portal
2. Walk through and run the Manifest in the **keda-k8s-manifest**directory
3. Deploy the Manifest
4. Refresh the Azure portal and the new config will be shown

## CICD

Create: https://github.com/AdminTurnedDevOps/cloud-native-prod-examples/blob/main/.github/workflows/deployKEDAWorkload.yml

Delete: https://github.com/AdminTurnedDevOps/cloud-native-prod-examples/blob/main/.github/workflows/deleteKEDACron.yml