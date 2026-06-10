import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/bert", tags=["bert"])

ARGO_SERVER_URL = "http://argo-workflows-server.argo.svc.cluster.local:2746/api/v1/workflows/kinootziv-app"


@router.post("/train")
async def start_training():
    payload = {
        "namespace": "kinootziv-app",
        "workflow": {
            "metadata": {"generateName": "bert-train-manual-", "namespace": "kinootziv-app"},
            "spec": {"workflowTemplateRef": {"name": "bert-train"}},
        },
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(ARGO_SERVER_URL, json=payload, timeout=10.0)

            if response.status_code in [200, 201]:
                data = response.json()
                return {"status": "success", "detail": f"Воркфлоу успешно запущен {data['metadata']['name']}"}

            else:
                raise HTTPException(status_code=response.status_code, detail=f"Argo API вернул ошибку: {response.text}")

        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Не удалось связаться с Argo Server: {str(e)}")


@router.get("/health")
async def health():
    pass


@router.post("/embeddings")
async def get_embeddings():
    pass


@router.post("/inference")
async def classify():
    pass


@router.post("/sft")
async def sft():
    pass


@router.post("/send_to_hf")
async def send_to_hf():
    pass
