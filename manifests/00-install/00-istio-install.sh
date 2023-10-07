#!/bin/bash

curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.19.1 TARGET_ARCH=x86_64 sh -

cd istio-1.19.1

export PATH=$PWD/bin:$PATH

istioctl install --set profile=demo -y

kubectl patch svc istio-ingressgateway -n istio-system --type='json' -p='[{"op": "replace", "path": "/spec/type", "value": "NodePort"}]'

cd $HOME

kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/download/v1.6.0/install.yaml

curl -LO https://github.com/argoproj/argo-rollouts/releases/download/v1.6.0/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts

