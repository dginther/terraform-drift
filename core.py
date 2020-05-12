import aws
import user


def users(statefile):
    auth = aws.get_session('iam')
    aws_users = user.get_aws_users(auth)
    state_users = user.get_state_users(statefile)
    diff = user.compare_users(aws_users, state_users)
    for u in diff:
        print(u)
