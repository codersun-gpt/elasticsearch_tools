"""Elasticsearch tools provider for Dify plugin."""

from typing import Any, Dict
from requests import RequestException
import json

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from helper.elasticsearch_helper import ElasticsearchHelper
from helper.auth_parser import parse_auth_list

class ElasticsearchToolsProvider(ToolProvider):
    """Provider for Elasticsearch API integration and credential validation."""
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            
            # TODO: 拆解， 用户配置 集群信息 [{"<clusterName>":"<clusterAddress>"}] 以及auth信息 [{"<clusterName>":"<authInfo>"}]
            # 不在集群信息中的不可以访问
            # Extract required credentials
            auth_list_text = credentials["auth_list"]  # 格式 [{"http://address:port":"username:password"}]
            
            # Parse the auth_list using the helper function
            auth_list = parse_auth_list(auth_list_text)

            # Check login for each cluster
            failed_clusters = []
            for auth_item in auth_list:
                cluster_address = auth_item.get("cluster_address")
                username = auth_item.get("username")
                password = auth_item.get("password")

                helper = ElasticsearchHelper(cluster_address, username, password)

                try:
                    helper.cluster_health()
                except RequestException as e:
                    failed_clusters.append({
                        "cluster_address": cluster_address,
                        "auth_info": auth_item,
                        "error": str(e)
                    })

            if failed_clusters:
                error_msg = "以下集群验证失败:\n" + "\n".join(
                    [f"集群地址 {c['cluster_address']}, 认证信息: {c['auth_info']}, 错误: {c['error']}" for c in failed_clusters]
                )
                raise ToolProviderCredentialValidationError(error_msg)

        except ToolProviderCredentialValidationError as e:
            raise e
        except KeyError as e:
            raise ToolProviderCredentialValidationError(f"缺少必需的认证信息: {str(e)}") from e
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"验证凭据时发生错误: {str(e)}") from e

    def _validate_input(self, auth_list: list) -> None:
        # Ensure auth_list contains valid cluster_address entries
        if not auth_list:
            raise ToolProviderCredentialValidationError("auth_list不能为空")

        for auth_item in auth_list:
            if not isinstance(auth_item, dict) or "cluster_address" not in auth_item:
                raise ToolProviderCredentialValidationError("auth_list中的每个项必须包含cluster_address字段")
