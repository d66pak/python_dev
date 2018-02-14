import boto3

"""
NOTE: Use list_objects_v2() instead of objects.all()
"""
s3 = boto3.session.Session(profile_name='default').resource('s3')
bucket = s3.Bucket('uat.au.vista.backup')
for obj in bucket.objects.all():
    print(obj.key)