import mimetypes
import boto3
from datetime import datetime
from typing import Iterator

from app.src.core.domain.document import RawDocument
from app.src.core.interfaces.source import BaseSourceResolver
from app.src.resolvers.s3.descriptor import S3SourceDescriptor
from app.src.resolvers.s3.streamable import S3Streamable


class S3SourceResolver(BaseSourceResolver):

    def discover(self, descriptor: S3SourceDescriptor) -> Iterator[RawDocument]:
        client = boto3.client(
            "s3",
            region_name=descriptor.region,
            aws_access_key_id=descriptor.aws_access_key_id,
            aws_secret_access_key=descriptor.aws_secret_access_key,
        )

        paginator = client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=descriptor.bucket, Prefix=descriptor.prefix):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                mime_type, _ = mimetypes.guess_type(key)
                yield RawDocument(
                    source_uri=f"s3://{descriptor.bucket}/{key}",
                    source_type="s3",
                    mime_type=mime_type,
                    content=S3Streamable(
                        bucket=descriptor.bucket,
                        key=key,
                        client=client,
                        chunk_size=descriptor.chunk_size,
                    ),
                    metadata={
                        "bucket": descriptor.bucket,
                        "key": key,
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "ingested_at": datetime.utcnow().isoformat(),
                    },
                )