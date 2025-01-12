1. Go to **Application scaling** under **Settings**
2. Click the blue **+ Create** button
3. Choose your workload
4. Under trigger type, choose Cron.
5. Set the min replicas to `0` and the max to `3`
6. Specify a time that's 2 minutes from what time it is now so you can see the scale occur