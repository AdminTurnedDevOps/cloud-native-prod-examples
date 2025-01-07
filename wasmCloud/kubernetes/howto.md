```
helm upgrade --install \
    wasmcloud-platform \
    --values https://raw.githubusercontent.com/wasmCloud/wasmcloud/main/charts/wasmcloud-platform/values.yaml \
    oci://ghcr.io/wasmcloud/charts/wasmcloud-platform \
    --dependency-update
```

check the deployment
```
kubectl rollout status deploy,sts -l app.kubernetes.io/name=nats

kubectl wait --for=condition=available --timeout=600s deploy -l app.kubernetes.io/name=wadm

kubectl wait --for=condition=available --timeout=600s deploy -l app.kubernetes.io/name=wasmcloud-operator
```