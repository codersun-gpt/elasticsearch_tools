import json
from typing import Any
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

def parse_auth_list(auth_list_text: str) -> list[dict[str, Any]]:
    """
    Parse the auth_list text into a structured list of authentication details.

    Args:
        auth_list_text (str): JSON string containing authentication details.

    Returns:
        list[dict[str, Any]]: Parsed authentication details.

    Raises:
        ToolProviderCredentialValidationError: If the input format is invalid.
    """
    auth_list = []

    try:
        raw_auth_list = json.loads(auth_list_text)
        # Convert the provided format to the expected format
        for auth_item in raw_auth_list:
            if isinstance(auth_item, dict):
                for cluster_address, auth in auth_item.items():
                    try:
                        if auth:  # 如果 auth 不为空，解析用户名和密码
                            username, password = auth.split(":")
                        else:  # 如果 auth 为空，表示未加密的集群
                            username, password = None, None
                        auth_list.append({
                            "cluster_address": cluster_address,
                            "username": username,
                            "password": password
                        })
                    except ValueError:
                        raise ToolProviderCredentialValidationError(
                            f"认证信息格式错误: {auth}, 应为 'username:password' 或为空"
                        )
    except json.JSONDecodeError:
        raise ToolProviderCredentialValidationError("auth_list必须是有效的JSON数组格式")

    return auth_list