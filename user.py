import json
from colorama import Fore, Back, Style, init

init(autoreset=True)


def get_aws_users(auth):
    users = auth.users.all()
    aws_users = []
    for user in users:
        attached_policies = []
        user_attached_policies = user.attached_policies.all()
        for policy in user_attached_policies:
            attached_policies.append(str.lower(policy.arn))
        aws_users.append({
            'user_id': str.lower(user.user_id),
            'user_name': str.lower(user.user_name),
            'arn': str.lower(user.arn),
            'attached_policies': attached_policies,
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
                        'arn': str.lower(instance['attributes']['arn']),
                        'attached_policies': []
                    })
        for resource in dict['resources']:
            if resource['type'] == "aws_iam_user" and resource['mode'] == "data":
                for instance in resource['instances']:
                    state_users.append({
                        'user_id': str.lower(instance['attributes']['id']),
                        'user_name': str.lower(instance['attributes']['user_name']),
                        'arn': str.lower(instance['attributes']['arn']),
                        'attached_policies': []
                    })
        for user in state_users:
            policy_list = []
            for resource in dict['resources']:
                if resource['type'] == "aws_iam_user_policy_attachment":
                    for instance in resource['instances']:
                        if str.lower(instance['attributes']['user']) == user['user_name']:
                            policy_list.append(
                                str.lower(instance['attributes']['policy_arn']))
            policy_list.sort()
    return state_users


def compare_users(list1, list2):
    aws_user_list = []
    state_user_list = []
    for aws_user in list1:
        aws_user_list.append(aws_user['user_name'])
    for state_user in list2:
        state_user_list.append(state_user['user_name'])
    print(Fore.GREEN + "Users in AWS not defined in Terraform State:")
    difference = list(set(aws_user_list) - set(state_user_list))
    difference.sort()
    for username in difference:
        print(Fore.RED + username)


def compare_user_policy_attachments(list1, list2):
    print(Fore.GREEN + "User Policy Attachments differences:")
    for item1 in list1:
        for item2 in list2:
            if item1['user_name'] == item2['user_name']:
                if item1['attached_policies'] != item2['attached_policies']:
                    print(Back.GREEN + item1['user_name'] + Style.RESET_ALL + ":\n" + Fore.GREEN + "AWS: " +
                          str(item1['attached_policies']) + "\n" + Fore.RED + "TF:  " + str(item2['attached_policies']) + Style.RESET_ALL)
