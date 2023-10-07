#!/bin/bash

kubectl label namespace default istio-injection=enabled

kubectl port-forward -n istio-system svc/kiali --address 0.0.0.0 20001:20001

cd ~
cd istio-1.19.1
kubectl apply -f samples/sleep/sleep.yaml
export SOURCE_POD=$(kubectl get pod -l app=sleep -o jsonpath={.items..metadata.name})

kubectl apply -f samples/httpbin/httpbin.yaml
kubectl exec "$SOURCE_POD" -c sleep -- curl -sS -v httpbin:8000/status/418


