import aws
import user
import group


def users(statefile):
    auth = aws.get_session('iam')
    aws_users = user.get_aws_users(auth)
    state_users = user.get_state_users(statefile)
    user.compare_users(aws_users, state_users)
    user.compare_user_policy_attachments(aws_users, state_users)


def groups(statefile):
    auth = aws.get_session('iam')
    aws_groups = group.get_aws_groups(auth)
    state_groups = group.get_state_groups(statefile)
    group.compare_groups(aws_groups, state_groups)


def group_policy_attachments(statefile):
    auth = aws.get_session('iam')
    aws_group_pol_att = group.get_aws_group_policy_attachments(auth)
    state_group_pol_att = group.get_state_group_policy_attachments(statefile)
    group.compare_group_policy_attachments(
        aws_group_pol_att, state_group_pol_att)
