helm install datadog -n datadog \
--set datadog.site='datadoghq.com' \
--set clusterName='aksenvironment01' \
--set logs.enabled=true \
--set logs.containerCollectAll=true \
--set datadog.apiKey='' \
--set processAgent.enabled=true \
--set targetSystem='linux' \
--set datadog.cws.enabled=true \
--set datadog.cspm.enabled=true \
--set datadog.cspm.hostBenchmarks.enabled=true \
--set datadog.securityAgent.runtime.enabled=true \
--set datadog.securityAgent.compliance.enabled=true \
--set datadog.securityAgent.compliance.host_benchmarks.enabled=true \
--set datadog.sbom.enabled=true \
--set datadog.sbom.containerImage.enabled=true \
--set datadog.sbom.host.enabled=true \
--set datadog.remoteConfiguration.enabled=true \
--set datadog.kubelet.tlsVerify=false \
datadog/datadog --create-namespace