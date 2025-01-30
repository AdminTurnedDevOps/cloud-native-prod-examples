## The App
1. Deploy the app you want to scale

For example, in the `app-deployment` directory, you can see a `deployment.yaml` that deploys an application which exists in Azure Container Registry (ACR).

## KEDA
If KEDA is not enabled already, you'll see a blue button that says **Enabled KEDA add-on**

1. Go to **Application scaling** under **Settings**
2. Click the blue **+ Create** button
3. Choose your workload
4. Under trigger type, choose Cron.
5. Set the min replicas to `0` and the max to `3`
6. Specify a time that's 2 minutes from what time it is now so you can see the scale occur