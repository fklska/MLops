# Kinootziv - сервис который классифицирует рецензии к фильмам

## Доступно по адресу: 
Для удобства и демонстрации через ingress-nginx были проброшены пути к админ панелям сервисов, можно посмотерть в манифесте ingress, а креды в соответствующих `ConfigMap`

Доступные пути:
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
#### Запуск Minikube:
В манифестах установлены требования - лимиты по запросам для подов: 2.6 cpu, 5610Mi RAM
Для джобы обучения: 1 cpu, 8Gi RAM
```
minikube start --driver=docker --cpus=4 --memory=20000mb --ports=80:80 --ports=443:443
minikube enable addons ingress-nginx
```
Проброс портов на 80 и 443 нужен для ingress, если у вас нет docker обертки, то поидее не нужен

#### Запуск приложения. 
```
git clone git@github.com:fklska/MLops.git
cd MLops
kubectl apply -f kubernetes/namespace.yaml
kubectl config set-context --current --namespace=kinootziv-app
kubectl apply -f kubernetes/core/ -R
```
ВАЖНО!!! в ingress-nginx настроен мой домен и поэтому ingress у вас может не работать. Тогда чтобы зайти в приложение или админ панели можно воспользоваться port-forward
`kubectl port-forward -n kinootziv-app svc/adminer-svc --address 0.0.0.0 8080:8080`

ВАЖНО!!! `Worker` при старте загружает модель из `mlflow` и `minio`, если там не будет модели, он не запуститься. Соответственно нужно запустить джобу по регистрации модели
`kubectl apply -f kubernetes/jobs/register-model.yaml` - джоба скачает базовую продовую модель с hf и зарегестрирует, модель весит 50мб.

ВАЖНО!!! `Backend` - запуститься, но если начать отправлять запросы он сломается так как в БД нет таблиц, соответсвенно нужно запустить джобу с миграциями: `kubectl apply -f kubernetes/jobs/postgres-migrations.yaml`

Джобы успешно отрабатают только если запущены соответсвующие поды для миграций это - postgres, для регистрации модели - mlflow, minio

#### Запуск ArgoCD
```
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f kubernetes/argocd/ -R
```

`kubectl get all` - просмотр состояния подов и сервисов в неймспесе который у вас установлен как текущий


### Вариант 2 - docker compose up
Меняете ветку на dev, там нет k8s, все поднимится в docker
```
git clone git@github.com:fklska/MLops.git
cd MLops
docker compose up -d
```

## [Архитектура](https://miro.com/app/board/uXjVGyP6Ul0=/?share_link_id=522725472856)
Приложение состоит из нескольких сервисов

