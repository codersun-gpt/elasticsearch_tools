# Elasticsearch Tools Plugin

A Dify plugin for interacting with Elasticsearch clusters.

## Features

- Authenticate with Elasticsearch clusters using username and password
- Perform REST API calls to Elasticsearch clusters
- Support for various Elasticsearch operations:
  - Cluster health checks
  - Index management
  - Search queries
  - Custom REST API calls

## Available Tools

### 1. Elasticsearch REST API Tool
- Perform REST API calls to Elasticsearch clusters
- Support for GET, POST, PUT, and DELETE methods
- Flexible input for custom endpoints and request bodies
- Output results in various formats (object, array, or string)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Elasticsearch credentials in the plugin settings:
- `cluster_info`: A JSON array mapping cluster names to their addresses. Example:
  ```json
  [{"cluster_name_1": "http://localhost:9200"}, {"cluster_name_2": "http://example.com:9200"}]
  ```
- `auth_list`: A JSON array mapping cluster names to their authentication information. Example:
  ```json
  [{"cluster_name_1": "username:password"}, {"cluster_name_2": "user:pass"}]
  ```

## Usage

### Elasticsearch REST API Tool

1. Perform a REST API call:
   - Specify the cluster name, endpoint, method, and request body
   - Supports GET, POST, PUT, and DELETE methods

Parameters:
- `cluster_name`: The name of the Elasticsearch cluster to call (e.g., `cluster_name_1`)
- `endpoint`: The API endpoint to call (e.g., `_cluster/health`)
- `method`: The HTTP method to use (`GET`, `POST`, `PUT`, or `DELETE`)
- `body`: The request body (optional, for POST and PUT methods)

Outputs:
- `success`: Indicates whether the API call was successful
- `error_message`: Error message if the request failed
- `result_object`: The response as an object (if applicable)
- `result_array`: The response as an array of objects (if applicable)
- `result_string`: The response as a string (if applicable)

## Development

The plugin consists of these main components:

1. `ElasticsearchToolsProvider`: Handles credential validation and cluster authentication
2. `ElasticsearchRest`: Handles REST API calls to Elasticsearch
3. `ElasticsearchHelper`: Provides helper methods for interacting with Elasticsearch clusters
4. Credential validation and error handling logic

## Error Handling

The plugin handles various error scenarios:
- Authentication failures
- Invalid cluster names or addresses
- Network connection issues
- API response errors
- Missing parameters
- Invalid credentials

## Contributing

GitHub: [CoderSun](https://github.com/codersun-gpt/elasticsearch_tools)



