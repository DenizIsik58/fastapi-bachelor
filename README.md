### Kubernetes

In order to host the application on Kubernetes, the project contains a kubernetes folder that contains the following files:

- `deployment.yaml` - The deployment file that contains the deployment configuration for the application.
- `service.yaml` - The service file that contains the service configuration for the application. This is used to expose the application to the outside world and it works as a load balancer between all your worker nodes.

Now, just like we specify the .env file in the docker-compose file, you need to run the following command to set up your secrets:

```
kubectl create configmap <name-of-configmap> --from-env-file=/path/to/.env
```

This will save the .env file as a configmap in your Kubernetes cluster. You can then reference this configmap in your deployment file by specifying the name.


in order to apply the deployment of the bachelor-api, run the following command:

```bash
kubectl apply -f kubernetes/deployment.yaml
```

The same goes for the load balancer:

```bash
kubectl apply -f kubernetes/service.yaml
```

To get an overview of all the pods, services and deployments, run the following command:

```bash
kubectl get all
```

for pods, run:

```bash
kubectl get pods
```

To debug or monitor logs, run the following command:

```bash
kubectl logs -f -l app=<name-of-deployment-label> --all-containers=true
```

for more information on how to deploy a docker container to Kubernetes, check out this [link](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/).