from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_rag_pipeline
from api.schemas.search import SearchResponse, SearchRequest, SourceResponse
from app.src.pipelines.rag_pipeline import RAGPipeline
from app.src.core.search.search_query import SearchQuery

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> SearchResponse:
    try:
        query = SearchQuery(text=request.query, top_k=request.top_k)
        result = await pipeline.run(query, top_n=request.top_n)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    sources = [
        SourceResponse(
            chunk_id=str(s.chunk.id),
            content=s.chunk.content,
            score=s.score,
            metadata=s.metadata,
        )
        for s in result.sources
    ]

    return SearchResponse(answer=result.answer, sources=sources)