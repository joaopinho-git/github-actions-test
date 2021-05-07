import os.path, requests, json
import load_configs

url=load_configs.file_configs["VAULT_URL"]
mount_point=load_configs.file_configs["VAULT_MOUNT_POINT"]
auth="Bearer "+load_configs.file_configs["VAULT_TOKEN"]
headers_vault = { 'Authorization': auth, 'Content-Type': 'application/json'}

#Put Role
def post_role(url, pbn, mount_point, headers_vault): 
    role_content = {
        "bound_service_account_names": pbn.replace("_","-"),
        "bound_service_account_namespaces": "*",
        "token_policies": [ pbn+"-policy" ]
    }
    final_url=url+"/v1/auth/"+mount_point+"/role/"+pbn
    try:
        r = requests.post(final_url, json=role_content, headers=headers_vault, verify = False)
        print("Status Code: {}".format(r.status_code))
        if r.status_code == 204:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(e)
        return False
    
