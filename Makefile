create_cluster:
	kind create cluster --config ./k8s/cluster/kind-cluster-config.yaml --name dev-cluster

deploy_redis:
	kubectl apply -f k8s/redis

delete_cluster:
	kind delete cluster --name dev-cluster

restart_cluster: delete_cluster create_cluster

.PHONY : help
help :
	@echo "create_cluster : Create kind cluster from config."
	@echo "deploy_redis : Deploy redis database in the redis namespace."
	@echo "delete_cluster: Delete kind cluster."
	@echo "restart_cluster: Restart kind cluster."