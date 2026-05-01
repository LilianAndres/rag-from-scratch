from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_ingestion_pipeline
from api.schemas.ingestion import IngestResponse, IngestRequest
from api.schemas.sources import LocalSourceRequest, S3SourceRequest
from app.src.core.domain.source import SourceDescriptor
from app.src.pipelines.ingestion_pipeline import IngestionPipeline
from app.src.resolvers.local.descriptor import LocalSourceDescriptor
from app.src.resolvers.s3.descriptor import S3SourceDescriptor

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


def _to_descriptor(source_request) -> SourceDescriptor:
    if isinstance(source_request, LocalSourceRequest):
        return LocalSourceDescriptor(
            path=source_request.path,
            glob_pattern=source_request.glob_pattern,
            recursive=source_request.recursive,
        )
    if isinstance(source_request, S3SourceRequest):
        return S3SourceDescriptor(
            bucket=source_request.bucket,
            prefix=source_request.prefix,
            region=source_request.region,
            aws_access_key_id=source_request.aws_access_key_id,
            aws_secret_access_key=source_request.aws_secret_access_key,
        )
    raise ValueError(f"Unknown source request type: {type(source_request)}")

@router.post("", response_model=IngestResponse)
async def ingest(
    request: IngestRequest,
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestResponse:
    try:
        descriptors = [_to_descriptor(s) for s in request.sources]
        await pipeline.ingest(descriptors)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return IngestResponse(message="Ingestion complete.")