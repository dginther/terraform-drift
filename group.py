import json
from colorama import Fore, Back, Style, init

init(autoreset=True)


def get_aws_groups(auth):
    groups = auth.groups.all()
    group_memberships = []
    for group in groups:
        g = auth.Group(group.name)
        user_list = []
        users = g.users.all()
        for user in users:
            user_list.append(str.lower(user.user_name))
        group_memberships.append({
            'group': str.lower(g.name),
            'users': user_list.sort()
        })
    return group_memberships


def get_state_groups(state):
    with (open(state, 'r')) as file:
        state_groups = []
        dict = json.load(file)
        for resource in dict['resources']:
            if resource['type'] == "aws_iam_group_membership" and resource['mode'] == "managed":
                for instance in resource['instances']:
                    state_groups.append({
                        'group': str.lower(instance['attributes']['name']),
                        'users': [x.lower() for x in instance['attributes']['users']].sort(),
                    })
    return state_groups


def get_aws_group_policy_attachments(auth):
    groups = auth.groups.all()
    group_policy_attachments = []
    for group in groups:
        g = auth.Group(group.name)
        policy_list = []
        policies = g.attached_policies.all()
        for policy in policies:
            policy_list.append(str.lower(policy.arn))
        policy_list.sort()
        group_policy_attachments.append({
            'group': str.lower(g.name),
            'policies': policy_list
        })
    return group_policy_attachments


def get_state_group_policy_attachments(state):
    with (open(state, 'r')) as file:
        state_group_policy_attachments = []
        dict = json.load(file)
        group_list = []
        for resource in dict['resources']:
            if resource['type'] == "aws_iam_group" and resource['mode'] == "managed":
                for instance in resource['instances']:
                    group_list.append(
                        str.lower(instance['attributes']['name']))
        for group in group_list:
            policy_list = []
            for resource in dict['resources']:
                if resource['type'] == "aws_iam_group_policy_attachment" and resource['mode'] == "managed":
                    for instance in resource['instances']:
                        if str.lower(instance['attributes']['group']) == group:
                            policy_list.append(
                                str.lower(instance['attributes']['policy_arn']))
            policy_list.sort()
            state_group_policy_attachments.append({
                'group': group,
                'policies': policy_list,
            })
    return state_group_policy_attachments


def compare_groups(list1, list2):
    print(Fore.GREEN + "Groups in AWS not defined in Terraform State:")
    groups = [item for item in list1 if item not in list2]
    for group in groups:
        print(Fore.RED + "Group: " +
              str(group['group']) + ", Users: " + str(group['users']))


def compare_group_policy_attachments(list1, list2):
    for item1 in list1:
        for item2 in list2:
            if item1['group'] == item2['group']:
                if item1['policies'] != item2['policies']:
                    print(Back.GREEN + item1['group'] + Style.RESET_ALL + ":\n" + Fore.GREEN + "AWS: " +
                          str(item1['policies']) + "\n" + Fore.RED + "TF:  " + str(item2['policies']) + Style.RESET_ALL)
