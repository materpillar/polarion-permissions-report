#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET


def get_all_permissions(roles):
    permissions = []
    tree = ET.parse('input.xml')
    root = tree.getroot()

    for role in roles:   
        role_element = root.find(".//role[@name='" + role +"']")
        grants_denies = list(role_element)
        for grant_deny in grants_denies:
            if grant_deny.attrib['permission'].replace("com.polarion.","") not in permissions:
                permissions.append(grant_deny.attrib['permission'].replace("com.polarion.",""))

    permissions.sort()
    return permissions


def gather_data(roles, permissions):
    permission_dict = dict.fromkeys(permissions)
    for permission in permissions:
        permission_dict[permission] = dict.fromkeys(roles)

    tree = ET.parse('input.xml')
    root = tree.getroot()
    for role in roles:   
        grants_denies = list(root.find(".//role[@name='" + role +"']"))
        for grant_deny in grants_denies:
            permission = grant_deny.attrib['permission'].replace("com.polarion.","")
            if grant_deny.tag == "deny":
                permission_dict[permission][role] = "\N{cross mark}"
            elif grant_deny.tag == "grant":
                permission_dict[permission][role] = "\N{check mark}"

    
    return permission_dict

def generate_html(roles, permissions, permission_dict):
    enviroment = Environment(loader=FileSystemLoader("templates"))

    results_filename = "data_results.html"
    results_template = enviroment.get_template("results.html")
    context = {
        "permissions": permissions,
        "roles": roles,
        "permission_dict": permission_dict
    }
    with open(results_filename, mode="w", encoding="utf-8") as results:
        results.write(results_template.render(context))
        print(f"Job done..")
        
def main():
    roles = ['project_admin', 'project_approver', 'project_user', 'project_assignable']
    permissions = get_all_permissions(roles)
    data = gather_data(roles, permissions)
    generate_html(roles, permissions, data)

if __name__ == "__main__":
    main()
