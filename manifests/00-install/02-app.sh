cd $HOME

kubectl create namespace messenger
kubectl create namespace frontend
kubectl label namespace messenger istio-injection=enabled
kubectl label namespace frontend istio-injection=enabled

mkdir repo
cd repo
git clone https://github.com/quinont/argo-rollout-example.git
cd argo-rollout-example/manifests/
