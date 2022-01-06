from minio import Minio
from cmdb.settings import MINIO_URL, MINIO_SSL, MINIO_USERNAME, MINIO_PASSWORD, MINIO_CONFIGFILE_BUCKET
from datetime import timedelta
minio_client = Minio(endpoint=MINIO_URL,
                     access_key=MINIO_USERNAME,
                     secret_key=MINIO_PASSWORD,
                     secure=MINIO_SSL)

#print(minio_client.list_buckets())
#print(minio_client.bucket_exists('test'))
#minio_client.make_bucket('test1','cn-north-1')
#minio_client.remove_object(bucket_name=MINIO_CONFIGFILE_BUCKET,object_name='ro31z0JvxtXS5jKiuQNUHMyaCRW7s6dLgpmfq9YTOF2VnkAB84')
#data = minio_client.get_object(bucket_name=MINIO_CONFIGFILE_BUCKET, object_name='I9PwdAD8QmRSfY4UVCyWpq5HJEoa6XOT2FzGLgrxkKuis7M10B')
#print(data.read().decode())
url = minio_client.presigned_get_object(MINIO_CONFIGFILE_BUCKET, 'E5NHAbCJP0V2jpfBqvwWym9Qo7r1T8SZYguMh4nitLIzs6cRlG', expires=timedelta(days=1))
print(url)