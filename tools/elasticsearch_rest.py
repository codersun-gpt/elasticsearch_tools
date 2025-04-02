from collections.abc import Generator
from typing import Any
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from helper.elasticsearch_helper import ElasticsearchHelper
from helper.auth_parser import parse_auth_list  # 引入解析函数

class ElasticsearchToolsTool(Tool):
    
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        cluster_address = tool_parameters.get("cluster_address")  
        endpoint = tool_parameters.get("endpoint")
        method = tool_parameters.get("method")
        body = tool_parameters.get("body")

        auth_list_text = self.runtime.credentials.get("auth_list", "[]")

        try:
            auth_list = parse_auth_list(auth_list_text)
        except Exception as e:
            yield self.create_variable_message("success", False)
            yield self.create_variable_message("error_message", f"Failed to parse auth_list: {str(e)}")
            return

        username = None
        password = None

        # allow empty username and password if cluster_address is not encrypted
        for item in auth_list:
            if item.get("cluster_address") == cluster_address:
                username = item.get("username")
                password = item.get("password")
                break

        helper = ElasticsearchHelper(cluster_address, username, password)
        try:
            result = helper._make_request(method, endpoint, json=body)
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