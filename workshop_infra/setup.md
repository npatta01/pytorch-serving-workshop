# Workshop Setup

The following included commands and steps that were used to create a working jupyter hub installation for the workshop.

The instructions assume that you are plannning to use GCP and have gcloud setup.


Most of the instructions are taken from [zero-to-jupyterhub](https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html) project.


## Step 1: common variables

```bash
REGION="us-east4"
ZONE="$REGION-a"
NODE_TYPE="n1-standard-2"

CLUSTER_NAME=workshop
NODES_MIN=0
NODES_MAX=200

EMAIL="npatta01@gmail.com"
GCP_PROJECT="np-public-training"

HELM_NAMESPACE=$CLUSTER_NAME

HELM_CHART_VERSION="1.2.0"
```

## Step 2: create static ip address

```bash
gcloud compute addresses create $CLUSTER_NAME \
    --region $REGION \
    --project $GCP_PROJECT

gcloud compute addresses describe $CLUSTER_NAME \
--region $REGION \
--project $GCP_PROJECT

```

Create an `A` record with your DNS provider.

I am using `hub` for my domain `np.training`



## Step 2b: Cert (optional)

By default the Helm chart we will use supports LetsEncrypt. However, I had trouble getting it to work.
So, I used followed the steps bellow to get create my own cert

create certificate signing request for "*.np.training"

```bash 
openssl req -nodes -newkey rsa:2048 \
-keyout cert/server.key \
-out cert/server.csr \
-subj "/C=US/ST=New York/L=New York/O=NP Training./OU=IT/CN=*.np.training"
```

I bought a wildcard cert from Namecheap


Download my cert and create a kubectl cert
```bash
gsutil cp "gs://np-training-private/certs/_star.np.training/*"  
cd cert

kubectl create secret tls $HELM_NAMESPACE-tls --key="tls.key" --cert="tls.crt" --namespace $HELM_NAMESPACE
cd ..
```




## Step 3: Create cluster


```bash

gcloud container clusters create \
  --machine-type n1-standard-2 \
  --num-nodes 2 \
  --zone $ZONE \
  --cluster-version latest \
  $CLUSTER_NAME \
  --project $GCP_PROJECT
```

Get kubectl credentials

```bash
gcloud container clusters get-credentials \
$CLUSTER_NAME \
--zone $ZONE \
--project $GCP_PROJECT
```

Create admin access for user

```bash
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole=cluster-admin \
  --user $EMAIL
```

Create separate node pool for jupyter notebook

```bash
gcloud beta container node-pools create user-pool \
  --machine-type $NODE_TYPE \
  --num-nodes 0 \
  --enable-autoscaling \
  --min-nodes $NODES_MIN \
  --max-nodes $NODES_MAX \
  --node-labels hub.jupyter.org/node-purpose=user \
  --node-taints hub.jupyter.org_dedicated=user:NoSchedule \
  --zone $ZONE \
  --cluster $CLUSTER_NAME  \
  --project $GCP_PROJECT
```

## Step 4: Helm setup

```bash

curl https://raw.githubusercontent.com/helm/helm/HEAD/scripts/get-helm-3 | bash

helm version

helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

```


## Step 5: Update config file (optional)


build docker image

```bash
docker build -t gcr.io/$GCP_PROJECT/pytorch-workshop:v1.0 .
docker push gcr.io/$GCP_PROJECT/pytorch-workshop:v1.0

```


encrypt setup
```

gcloud kms keyrings create sops --location global --project $GCP_PROJECT
gcloud kms keys create sops-key --location global --keyring sops --purpose encryption --project $GCP_PROJECT
gcloud kms keys list --location global --keyring sops --project $GCP_PROJECT
```


```

sops --encrypt --gcp-kms projects/$GCP_PROJECT/locations/global/keyRings/sops/cryptoKeys/sops-key \
--encrypted-regex '^(client_id|client_secret)$' \
workshop_infra/config.yaml > workshop_infra/config.enc.yaml
```


```
sops --decrypt workshop_infra/config.enc.yaml > workshop_infra/config.yaml
```


replace values in [config.yaml](workshop_infra/config.yaml)

- GitHubOAuthenticator
- singleuser.image.name
- scheduling.userPlaceholder.replicas
- proxy.https.host
- proxy.https.service.loadBalancerIP



## Step 6: Helm Install


```
helm upgrade --cleanup-on-fail \
  --install $HELM_NAMESPACE jupyterhub/jupyterhub \
  --namespace $HELM_NAMESPACE \
  --create-namespace \
  --version $HELM_CHART_VERSION \
  --values config.yaml

```

```
kubectl --namespace=$HELM_NAMESPACE get pod

kubectl --namespace=$HELM_NAMESPACE  get svc proxy-public -o jsonpath='{.status.loadBalancer.ingress[].ip}'
```

