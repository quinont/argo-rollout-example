cd $HOME/istio-1.19.1/samples/addons/
kubectl apply -f prometheus.yaml
kubectl apply -f kiali.yaml
kubectl apply -f jaeger.yaml
kubectl apply -f grafana.yaml
