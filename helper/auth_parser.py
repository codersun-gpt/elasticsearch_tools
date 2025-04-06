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
        for auth_item in raw_auth_list:
            if isinstance(auth_item, dict):
                for cluster_name, auth in auth_item.items():  # Key is now cluster_name
                    try:
                        if auth:
                            username, password = auth.split(":")
                        else:
                            username, password = None, None
                        auth_list.append({
                            "cluster_name": cluster_name,  # Use cluster_name as the key
                            "username": username,
                            "password": password
                        })
                    except ValueError:
                        raise ToolProviderCredentialValidationError(
                            f"Invalid auth format: {auth}, expected 'username:password' or empty"
                        )
    except json.JSONDecodeError:
        raise ToolProviderCredentialValidationError("auth_list must be a valid JSON array")

    return auth_list

def parse_cluster_info(cluster_info_text: str) -> dict[str, str]:
    """
    Parse the cluster_info text into a mapping of cluster names to addresses.

    Args:
        cluster_info_text (str): JSON string containing cluster information.

    Returns:
        dict[str, str]: Mapping of cluster names to addresses.

    Raises:
        ToolProviderCredentialValidationError: If the input format is invalid.
    """
    try:
        cluster_info = json.loads(cluster_info_text)
        if not isinstance(cluster_info, list) or not all(isinstance(item, dict) for item in cluster_info):
            raise ValueError("cluster_info必须是字典列表")
        return {list(item.keys())[0]: list(item.values())[0] for item in cluster_info}
    except json.JSONDecodeError:
        raise ToolProviderCredentialValidationError("cluster_info必须是有效的JSON数组格式")
    except Exception as e:
        raise ToolProviderCredentialValidationError(f"解析cluster_info时发生错误: {str(e)}")

def get_auth_for_cluster(auth_list: list[dict[str, Any]], cluster_name: str) -> dict[str, Any]:
    """
    Get the authentication information for a specific cluster.

    Args:
        auth_list (list[dict[str, Any]]): List of authentication details.
        cluster_name (str): Name of the cluster.

    Returns:
        dict[str, Any]: Authentication details for the cluster. If not found, returns default values.

    """
    for item in auth_list:
        if item.get("cluster_name") == cluster_name:
            return item
    # Return default authentication info if the cluster_name is not found
    return {
        "cluster_name": cluster_name,
        "username": None,
        "password": None
    }