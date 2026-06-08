# Kinootziv - сервис который классифицирует рецензии к фильмам

## Доступно по адресу:
Для удобства и демонстрации через ingress-nginx были проброшены пути к админ панелям сервисов, можно посмотерть в манифесте ingress, а креды в соответствующих `ConfigMap`

```
/backend/
/mlflow/
/grafana/
/adminer/
/prometheus/
/argocd/
```

## Как запускать?
### Вариант 1 - через k8s / Minikube
```
git clone git@github.com:fklska/MLops.git
cd MLops
minikube start --driver=docker --cpus=4 --memory=20000mb --ports=80:80 --ports=443:443
minikube enable addons ingress-nginx
kubectl apply -f kubernetes/namespace.yaml
kubectl config set-context --current --namespace=kinootziv-app
// kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml # Optional
kubectl apply -f kubernetes/ -R
```
Проброс портов нужен для ingress, если у вас нет docker обертки, то поидее не нужен

У вас запустятся и деплойменты и джобы, соответственно джобы успешно отрабатают только если запущены соответсвующие поды для миграций это - postgres, для регистрации модели - mlflow, minio

`kubectl get all` - просмотр состояния подов и сервисов


### Вариант 2 - docker compose up
Меняете ветку на dev, там нет k8s, все поднимится в docker
```
git clone git@github.com:fklska/MLops.git
cd MLops
docker compose up -d
```

## [Архитектура](https://miro.com/app/board/uXjVGyP6Ul0=/?share_link_id=522725472856)
Приложение состоит из нескольких сервисов
