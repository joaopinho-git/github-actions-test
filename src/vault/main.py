import requests, yaml
import load_configs, async_hvac_calls as hvac, vault_api_calls as api
import asyncio

auth_vault="Bearer "+load_configs.file_configs["VAULT_TOKEN"]
headers_vault = { 'Authorization': auth_vault, 'Content-Type': 'application/json'}

async def main():
    applications=get_githubfile()
    await create_vault_requirements(applications)
    
def get_githubfile():
    auth_github="Bearer "+load_configs.file_configs["GITHUB_KEY"]
    headers_github = { 'Authorization': auth_github, 'Accept': 'application/vnd.github.v3.raw'}

    

    resp_repo_values = requests.get("https://api.github.com/repos/farfetch-internal/it-apps-argocd/contents/appsargocd/values.yaml?ref=master", headers=headers_github, verify = False)
    dictionary = yaml.load(resp_repo_values.text, Loader=yaml.FullLoader)

    applications = []
    for key, value in dictionary.items():
        if key == "applications":
            for l in dictionary[key]:
                applications.append(l["name"])
    return applications

async def create_vault_requirements(applications): 
    for app in applications:
        app_name=app.replace("-","_")
        
        #check if secret exists
        result_get = await hvac.get_secrets(app_name)
        if result_get is True:
            print("Secret for {} already exists, skipping creation.".format(app_name))
        else:
            print("Secret for {} does not exist, creating...".format(app_name))
            #put secret
            result_put = await hvac.put_secrets(app_name)
            if result_put is True:
                print("Success adding {} secret.".format(app_name))
            else:
                print("Error adding {} secret.".format(app_name))
        
        #check if policy exists
        get_policy_result = await hvac.get_policy(app_name)
        if get_policy_result is True:
            print("Policy for {} already exists, skipping creation.".format(app_name))
        else:
            print("Policy for {} does not exist, creating...".format(app_name)) 
            await hvac.put_policy(app_name)
        
        #check if role exists
        role_result = await hvac.get_role(app_name)
        if role_result is True:
            print("Role for {} already exists, skipping creation.".format(app_name))
        else:
            print("Role for {} does not exist, creating...".format(app_name)) 
            result_post_role = api.post_role(load_configs.file_configs["VAULT_URL"], app_name, load_configs.file_configs["VAULT_MOUNT_POINT"], headers_vault)
            if result_post_role is True:
                print("Success adding {} role.".format(app_name))
            else:
                print("Error adding {} role.".format(app_name))

if __name__ == "__main__": 
    asyncio.run(main())