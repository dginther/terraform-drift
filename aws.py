import boto3
from botocore.exceptions import ClientError


def get_session(session_type):
    try:
        session = boto3.session.Session()
        auth = session.resource(session_type)
    except ClientError as e:
        print("Error: %s" % e)
    return auth
