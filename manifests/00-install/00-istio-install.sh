#!/bin/bash

curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.19.1 TARGET_ARCH=x86_64 sh -

cd istio-1.19.1

export PATH=$PWD/bin:$PATH

istioctl install --set profile=demo -y

kubectl patch svc istio-ingressgateway -n istio-system --type='json' -p='[{"op": "replace", "path": "/spec/type", "value": "NodePort"}]'

kubectl create namespace messenger 
kubectl create namespace frontend

kubectl label namespace messenger istio-injection=enabled
kubectl label namespace frontend istio-injection=enabled

cd samples/addons/
