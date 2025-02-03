"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Create an AWS resource (S3 Bucket)
bucket = s3.BucketV2('devops4life-pulumi-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

# Create an S3 Bucket object
website = s3.BucketWebsiteConfigurationV2("website",
    bucket=bucket.id,
    index_document={
        "suffix": "index.html",
    })

ownership_controls = s3.BucketOwnershipControls(
    'ownership-controls',
    bucket=bucket.id,
    rule={
        "object_ownership": 'ObjectWriter',
    },
)

public_access_block = s3.BucketPublicAccessBlock(
    'public-access-block', bucket=bucket.id, block_public_acls=False
)

bucket_object = s3.BucketObject(
    'index.html',
    bucket=bucket.id,
    source=pulumi.FileAsset('index.html'),
    content_type='text/html',
    acl='public-read',
    opts=pulumi.ResourceOptions(depends_on=[public_access_block, ownership_controls, website]),
)

pulumi.export('bucket_endpoint', pulumi.Output.concat('http://', website.website_endpoint))
