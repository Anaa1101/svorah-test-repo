"""X-REGION-HINT | when a region literal is actually in the source, the code agent grabs
it as a HINT and still only says "suspected" (the real datacenter is a runtime fact the
cloud agent confirms). ap-south-1 = India hint; us-east-1 = foreign hint."""
import boto3

from app.models.user import User


def foreign_region(user: User):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.put_object(Bucket="scans", Key="k", Body=user.aadhaar)   # region hint us-east-1 -> SUSPECTED cross-border


def india_region(user: User):
    s3 = boto3.client("s3", region_name="ap-south-1")
    s3.put_object(Bucket="scans", Key="k", Body=user.aadhaar)   # region hint ap-south-1 -> not_suspected (in-India hint)
