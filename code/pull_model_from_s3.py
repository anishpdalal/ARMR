import boto3
from user_definition import bucket_name

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
models = []
for o in bucket.objects.all():
    models.append(o.key)
models = sorted(models)
model = models[0]

try:
    bucket.download_file(model, model)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
