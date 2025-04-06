from collections.abc import Generator
from typing import Any
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from helper.elasticsearch_helper import ElasticsearchHelper
from helper.auth_parser import parse_cluster_info, parse_auth_list, get_auth_for_cluster

class ElasticsearchRest(Tool):  
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        cluster_name = tool_parameters.get("cluster_name")
        endpoint = tool_parameters.get("endpoint")
        method = tool_parameters.get("method")
        body = tool_parameters.get("body")
        timeout = tool_parameters.get("timeout", 10)

        cluster_info_text = self.runtime.credentials.get("cluster_info", "[]")
        auth_list_text = self.runtime.credentials.get("auth_list", "[]")

        try:
            cluster_map = parse_cluster_info(cluster_info_text)
            auth_list = parse_auth_list(auth_list_text)
        except ToolProviderCredentialValidationError as e:
            yield self.create_variable_message("success", False)
            yield self.create_variable_message("error_message", f"Failed to parse credentials: {str(e)}")
            return

        if cluster_name not in cluster_map:
            yield self.create_variable_message("success", False)
            yield self.create_variable_message("error_message", f"Cluster '{cluster_name}' is not in cluster_info")
            return

        cluster_address = cluster_map[cluster_name]
        try:
            auth_info = get_auth_for_cluster(auth_list, cluster_name)
            username, password = auth_info["username"], auth_info["password"]
        except ToolProviderCredentialValidationError as e:
            yield self.create_variable_message("success", False)
            yield self.create_variable_message("error_message", str(e))
            return

        helper = ElasticsearchHelper(cluster_address, username, password)
        try:
            result = helper._make_request(method, endpoint, timeout=timeout, json=body)
        except Exception as e:
            yield self.create_variable_message("success", False)
            yield self.create_variable_message("error_message", f"Request failed: {str(e)}")
            return

        yield self.create_variable_message("success", True)
        if isinstance(result, dict):
            yield self.create_variable_message("result_object", result)
        elif isinstance(result, list):
            yield self.create_variable_message("result_array", result)
        else:
            yield self.create_variable_message("result_string", str(result))