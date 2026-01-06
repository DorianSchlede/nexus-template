# Beam API Reference

Complete API documentation for Beam AI platform.

## Base URL

```
https://api.beamstudio.ai
```

## Authentication

All requests require:
- `Authorization: Bearer {access_token}` - Token from /auth/access-token
- `current-workspace-id: {workspace_id}` - Your workspace ID

---

## Authentication Endpoints (2)

### POST /auth/access-token
Exchange API key for access token.

**Request:**
```json
{"apiKey": "bm_key_xxxxxxxxxxxxx"}
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### POST /auth/refresh-token
Refresh an expired access token.

**Request:**
```json
{"refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## User Endpoints (1)

### GET /v2/user/me
Get current user profile.

**Response:**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```

---

## Agent Endpoints (1)

### GET /agent
List all agents in workspace.

**Query Parameters:**
- None required

**Response:**
```json
[
  {
    "id": "agent-uuid",
    "name": "Customer Support Agent",
    "description": "Handles customer inquiries",
    "type": "beam-os",
    "createdAt": "2024-01-15T10:30:00Z"
  }
]
```

---

## Agent Context Files (1)

### GET /agent/{agentId}/context/file/{fileId}/download
Download agent context file.

**Path Parameters:**
- `agentId` - Agent UUID
- `fileId` - File UUID

**Response:** File binary data

---

## Agent Graph Endpoints (4)

### GET /agent-graphs/{agentId}
Get agent workflow graph.

**Path Parameters:**
- `agentId` - Agent UUID

**Query Parameters:**
- `graphId` (optional) - Specific graph version

**Response:**
```json
{
  "graph": {
    "agentId": "agent-uuid",
    "nodes": [...],
    "isActive": true,
    "isPublished": true
  }
}
```

### POST /agent-graphs/test-node
Test a specific graph node.

**Request:**
```json
{
  "agentId": "agent-uuid",
  "nodeId": "node-uuid",
  "graphId": "graph-uuid",
  "params": {
    "input": "test data"
  }
}
```

### PATCH /agent-graphs/update-node
Update node configuration.

**Request:**
```json
{
  "nodeId": "node-uuid",
  "objective": "New objective",
  "evaluationCriteria": ["Criteria 1", "Criteria 2"],
  "onError": "STOP"
}
```

### GET /agent-graphs/agent-task-nodes/{toolFunctionName}
Get nodes using a specific tool.

**Path Parameters:**
- `toolFunctionName` - Tool function name (e.g., "send_email")

**Query Parameters:**
- `agentId` (optional) - Filter by agent
- `isRated` (optional) - Filter rated nodes only
- `pageNum`, `pageSize` - Pagination

---

## Agent Task Endpoints (13)

### GET /agent-tasks
List tasks with filtering.

**Query Parameters:**
- `pageNum` - Page number (default: 1)
- `pageSize` - Items per page (default: 10)
- `agentId` - Filter by agent
- `statuses` - Comma-separated statuses (e.g., "QUEUED,COMPLETED,FAILED")
- `searchQuery` - Search in task names
- `ordering` - Sort order (e.g., "createdAt:desc")
- `startDate`, `endDate` - Date range filter
- `grouping` - Group results (e.g., "status")

### POST /agent-tasks
Create new task.

**Request:**
```json
{
  "agentId": "agent-uuid",
  "taskQuery": "Send email to john@example.com with meeting notes",
  "parsingUrls": ["https://example.com/notes.pdf"],
  "encodedContextFiles": []
}
```

**Response:**
```json
{
  "id": "task-uuid",
  "customId": "AGE-785",
  "status": "QUEUED",
  "updatesUrl": "https://api.beamstudio.ai/agent-tasks/task-uuid/updates"
}
```

### GET /agent-tasks/{taskId}
Get task details.

### GET /agent-tasks/{taskId}/updates
Stream task updates (SSE).

**Note:** Returns Server-Sent Events for real-time updates.

### GET /agent-tasks/analytics
Get agent analytics.

**Query Parameters:**
- `agentId` - Agent to analyze
- `startDate`, `endDate` - Analysis period

**Response:**
```json
{
  "currentPeriod": {
    "totalTasks": 150,
    "completedTasks": 135,
    "failedTasks": 15,
    "averageEvaluationScore": 87.5,
    "averageRuntimeSeconds": 45.7
  },
  "metricsDelta": {
    "totalTasksDelta": "+15.5%"
  }
}
```

### GET /agent-tasks/latest-executions
Get recent task executions.

### GET /agent-tasks/iterate
Iterate through tasks (cursor-based pagination).

### GET /agent-tasks/tool-output-schema/{graphNodeId}
Get expected output schema for a tool node.

### POST /agent-tasks/retry
Retry a failed task.

**Request:**
```json
{
  "taskId": "task-uuid"
}
```

### PATCH /agent-tasks/execution/{taskId}/user-input
Provide user input for HITL task.

**Request:**
```json
{
  "input": "User's response to agent question"
}
```

### POST /agent-tasks/execution/{taskId}/rejection
Reject a task execution.

### POST /agent-tasks/execution/{taskId}/user-consent
Approve a HITL task.

### PATCH /agent-tasks/execution/{taskId}/output-rating
Rate task output quality.

**Request:**
```json
{
  "taskNodeId": "node-uuid",
  "rating": "positive",
  "userFeedback": "Task completed correctly",
  "expectedOutput": "Optional expected output"
}
```

---

## Tool Endpoints (2)

### POST /tool/optimize/{toolFunctionName}
Start tool optimization.

**Path Parameters:**
- `toolFunctionName` - Tool to optimize

### POST /tool/optimization-status/thread/{threadId}
Check optimization status.

**Path Parameters:**
- `threadId` - Optimization thread ID

---

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Rate Limited - Too many requests |
| 500 | Server Error |

---

## Rate Limits

- Default: 100 requests/minute per workspace
- Burst: Up to 10 requests/second
- Long-running operations may have lower limits

---

## Python Example

```python
import requests

# Get access token
auth = requests.post(
    'https://api.beamstudio.ai/auth/access-token',
    json={'apiKey': 'bm_key_xxx'}
)
token = auth.json()['idToken']

# Make API request
headers = {
    'Authorization': f'Bearer {token}',
    'current-workspace-id': 'workspace-uuid'
}

# List agents
agents = requests.get(
    'https://api.beamstudio.ai/agent',
    headers=headers
)
print(agents.json())
```
