import json


def get_aws_users(auth):
    users = auth.users.all()
    aws_users = []
    for user in users:
        aws_users.append({
            'user_id': str.lower(user.user_id),
            'user_name': str.lower(user.user_name),
            'arn': str.lower(user.arn),
        })
    return aws_users


def get_state_users(state):
    with (open(state, 'r')) as file:
        state_users = []
        dict = json.load(file)
        for resource in dict['resources']:
            if resource['type'] == "aws_iam_user" and resource['mode'] == "managed":
                for instance in resource['instances']:
                    state_users.append({
                        'user_id': str.lower(instance['attributes']['unique_id']),
                        'user_name': str.lower(instance['attributes']['name']),
                        'arn': str.lower(instance['attributes']['arn'])
                    })
        for resource in dict['resources']:
            if resource['type'] == "aws_iam_user" and resource['mode'] == "data":
                for instance in resource['instances']:
                    state_users.append({
                        'user_id': str.lower(instance['attributes']['id']),
                        'user_name': str.lower(instance['attributes']['user_name']),
                        'arn': str.lower(instance['attributes']['arn'])
                    })
    return state_users


def compare_users(list1, list2):
    difference = []
    for i in list1:
        if i not in list2:
            difference.append(i)
    return difference
