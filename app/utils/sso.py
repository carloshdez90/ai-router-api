import requests


def validate_token(token, env_vars):
    url = f'{env_vars["sso_url"]}auth/realms/{env_vars["sso_realm"]}/protocol/openid-connect/token/introspect'
    payload = {
        'token_type_hint': 'requesting_party_token',
        'token': token
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Authorization": f"Basic {env_vars['sso_key']}"}

    response = requests.post(url, headers=headers, data=payload)
    return response
