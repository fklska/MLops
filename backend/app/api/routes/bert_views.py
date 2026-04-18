from fastapi import APIRouter

router = APIRouter(prefix="/bert", tags=["bert"])


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
