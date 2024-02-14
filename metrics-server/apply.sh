#kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# Doing the above means the metric server does not run inside Docker Desktop because
# it raises 503s - because of a certificate error.

# $response = Invoke-WebRequest https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# $contentString = [System.Text.Encoding]::UTF8.GetString($response.Content)
# $contentString | Out-File -FilePath components.yaml -Encoding UTF8

# ... Now done manually beforehand ...
# curl -L https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml >> components.yaml
kubectl apply -f ./components.yaml