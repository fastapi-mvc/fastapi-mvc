#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

DIR=$(cd $(dirname "${BASH_SOURCE}") && pwd -P)

if ! command -v minikube &> /dev/null; then
  echo "minikube is not installed"
  exit 1
fi

if ! command -v kubectl &> /dev/null; then
  echo "kubectl is not installed"
  exit 1
fi

HELM_VERSION=$(helm version 2>&1 | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+') || true
if [[ ${HELM_VERSION} < "v3.0.0" ]]; then
  echo "Please upgrade helm to v3.0.0 or higher"
  exit 1
fi

KUBE_CLIENT_VERSION=$(kubectl version --client --short | awk '{print $3}' | cut -d. -f2) || true
if [[ ${KUBE_CLIENT_VERSION} -lt 16 ]]; then
  echo "Please update kubectl to 1.16 or higher"
  exit 1
fi

echo "[dev-env] starting minikube"
MINIKUBE_IN_STYLE=0 minikube start --driver=docker 2>/dev/null

echo "[dev-env] enabling ingress addon"
minikube addons enable ingress

echo "[dev-env] enabling ssl-passthrough for ingress controller"
# Check deployment rollout status every 10 seconds (max 10 minutes) until complete.
ATTEMPTS=0
ROLLOUT_STATUS_CMD="kubectl rollout status deployment/ingress-nginx-controller -n ingress-nginx"
until $ROLLOUT_STATUS_CMD || [ $ATTEMPTS -eq 60 ]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  sleep 10
done

INGRESS_HOST="$(minikube ip).nip.io"

echo "[dev-env] pushing app image"
minikube image load "{{ cookiecutter.folder_name }}:${TAG}"

echo "[dev-env] creating {{ cookiecutter.folder_name }} namespace"
kubectl create namespace {{ cookiecutter.folder_name }}

ATTEMPTS=0
ROLLOUT_STATUS_CMD="kubectl get namespace {{ cookiecutter.folder_name }} -n {{ cookiecutter.folder_name }}"
until $ROLLOUT_STATUS_CMD 2>/dev/null || [ $ATTEMPTS -eq 60 ]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  sleep 10
done
{% if cookiecutter.redis == "yes" %}
# Install Redis operator
echo "[dev-env] creating redis-operator"
kubectl create -f manifests/all-redis-operator-resources.yaml

ATTEMPTS=0
ROLLOUT_STATUS_CMD="kubectl rollout status deployment.apps/redisoperator"
until $ROLLOUT_STATUS_CMD 2>/dev/null || [ $ATTEMPTS -eq 60 ]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  sleep 10
done

kubectl create -f manifests/persistent-storage-no-pvc-deletion.yaml -n {{ cookiecutter.folder_name }}

ATTEMPTS=0
ROLLOUT_STATUS_CMD="kubectl rollout status deployment.apps/rfs-redisfailover-persistent-keep -n {{ cookiecutter.folder_name }}"
until $ROLLOUT_STATUS_CMD || [ $ATTEMPTS -eq 60 ]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  sleep 10
done

echo "[dev-env] Checking redis-operator statefulset replicas status to be ready"
STATEFULSET_REPLICAS=$(kubectl get statefulset rfr-redisfailover-persistent-keep -o jsonpath='{.spec.replicas}' -n {{ cookiecutter.folder_name }})
ATTEMPTS=0
until [[ ${STATEFULSET_REPLICAS} -eq $(kubectl get statefulset rfr-redisfailover-persistent-keep -o jsonpath='{.status.readyReplicas}' -n {{ cookiecutter.folder_name }}) ]] || [ $ATTEMPTS -eq 60 ]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  sleep 10
done

echo "[dev-env] installing {{ cookiecutter.folder_name }} charts"
helm upgrade --install \
    {{ cookiecutter.folder_name }} charts/{{ cookiecutter.chart_name }} \
    --namespace {{ cookiecutter.folder_name }} \
    --set ingress.host.name="{{ cookiecutter.folder_name }}.${INGRESS_HOST}"
{% else %}
echo "[dev-env] installing {{ cookiecutter.folder_name }} charts"
helm upgrade --install \
    {{ cookiecutter.folder_name }} charts/{{ cookiecutter.chart_name }} \
    --namespace {{ cookiecutter.folder_name }} \
    --set ingress.host.name="{{ cookiecutter.folder_name }}.${INGRESS_HOST}" \
    --set configMap.useRedis="false"
{% endif %}
ATTEMPTS=0
ROLLOUT_STATUS_CMD="kubectl rollout status deployment/{{ cookiecutter.folder_name }} -n {{ cookiecutter.folder_name }}"
until $ROLLOUT_STATUS_CMD || [ $ATTEMPTS -eq 60 ]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  sleep 10
done

cat <<EOF
Kubernetes cluster ready
FastAPI available under: http://{{ cookiecutter.folder_name }}.${INGRESS_HOST}/
You can delete dev-env by issuing: make clean
EOF
