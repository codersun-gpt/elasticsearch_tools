"""Elasticsearch tools provider for Dify plugin."""

from typing import Any, Dict
from requests import RequestException
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from helper.elasticsearch_helper import ElasticsearchHelper
from helper.auth_parser import parse_cluster_info, parse_auth_list, get_auth_for_cluster

class ElasticsearchToolsProvider(ToolProvider):
    """Provider for Elasticsearch API integration and credential validation."""
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # Extract and parse cluster information and authentication information
            cluster_info_text = credentials["cluster_info"]
            auth_list_text = credentials["auth_list"]

            cluster_map = parse_cluster_info(cluster_info_text)
            auth_list = parse_auth_list(auth_list_text)

            # Check login for each cluster
            failed_clusters = []
            for cluster_name, cluster_address in cluster_map.items():
                try:
                    auth_info = get_auth_for_cluster(auth_list, cluster_name)
                    username, password = auth_info["username"], auth_info["password"]
                except ToolProviderCredentialValidationError as e:
                    failed_clusters.append({
                        "cluster_name": cluster_name,
                        "error": str(e)
                    })
                    continue

                helper = ElasticsearchHelper(cluster_address, username, password)
                try:
                    helper.cluster_health()
                except RequestException as e:
                    failed_clusters.append({
                        "cluster_name": cluster_name,
                        "cluster_address": cluster_address,
                        "error": str(e)
                    })

            if failed_clusters:
                error_msg = "The following clusters failed validation:\n" + "\n".join(
                    [f"Cluster Name: {c['cluster_name']}, Address: {c.get('cluster_address', 'Unknown')}, Error: {c['error']}" for c in failed_clusters]
                )
                raise ToolProviderCredentialValidationError(error_msg)

        except ToolProviderCredentialValidationError as e:
            raise e
        except KeyError as e:
            raise ToolProviderCredentialValidationError(f"Missing required credential information: {str(e)}") from e
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"An error occurred while validating credentials: {str(e)}") from e
