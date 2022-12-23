# Kubernetes
hw4

В проекте используются докер образы:
```
skienbear/online-inference:v1
skienbear/online-inference:v2
```
Деплой приложений:
```
kubectl apply -f online-inference-pod.yaml
kubectl apply -f online-inference-pod-resources.yaml
kubectl apply -f online-inference-pod-probes.yaml
kubectl apply -f online-inference-replicaset.yaml
kubectl apply -f online-inference-deployment-blue-green.yaml
kubectl apply -f online-inference-deployment-rolling-update.yaml
```

Удалить приложение:
```
kubectl delete -f <app name>.yaml
```

Посмотреть поды:
```
kubectl get pods
```

Визуальный просмотр:
```
minikube dashboard
```

Для запуска helm зайти в папку .helm и установить:
```
helm install online-inference ./online-inference
```





