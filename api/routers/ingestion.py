from fastapi import APIRouter, Depends, HTTPException

from api.schemas import IngestRequest, IngestResponse
from api.dependencies import get_ingestion_pipeline
from app.src.pipelines.ingestion_pipeline import IngestionPipeline

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("", response_model=IngestResponse)
async def ingest(
    request: IngestRequest,
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestResponse:
    try:
        await pipeline.ingest(request.sources)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return IngestResponse(
        message="Ingestion complete.",
        ingested=request.sources,
    )