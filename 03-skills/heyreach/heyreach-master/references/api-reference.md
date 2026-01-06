# HeyReach API Reference

Complete endpoint documentation for HeyReach API.

---

## Base Configuration

| Property | Value |
|----------|-------|
| Base URL | `https://api.heyreach.io/api/public` |
| Auth Header | `X-API-KEY: {api_key}` |
| Content Type | `application/json` |
| Rate Limit | 300 requests/minute |

---

## Authentication

All requests require the `X-API-KEY` header:

```http
X-API-KEY: your-api-key-here
Content-Type: application/json
```

### Check API Key
```http
GET /auth/CheckApiKey
```
Returns 200 if API key is valid.

---

## Endpoints

### Campaigns

#### List All Campaigns
```http
POST /campaign/GetAll
```

**Request Body:**
```json
{
  "offset": 0,
  "limit": 100
}
```

**Response:**
```json
{
  "items": [
    {
      "id": "campaign-id",
      "name": "Campaign Name",
      "status": "ACTIVE",
      "createdAt": "2025-01-01T00:00:00Z"
    }
  ],
  "totalCount": 50
}
```

---

#### Get Campaign Details
```http
POST /campaign/GetById
```

**Request Body:**
```json
{
  "campaignId": "campaign-id"
}
```

---

#### Pause Campaign
```http
POST /campaign/Pause
```

**Request Body:**
```json
{
  "campaignId": "campaign-id"
}
```

---

#### Resume Campaign
```http
POST /campaign/Resume
```

**Request Body:**
```json
{
  "campaignId": "campaign-id"
}
```

---

### Leads

#### Add Leads to Campaign
```http
POST /campaign/AddLeadsToCampaign
```

**Request Body:**
```json
{
  "campaignId": "campaign-id",
  "leads": [
    {
      "profileUrl": "https://linkedin.com/in/username",
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com"
    }
  ]
}
```

---

#### Get Campaign Leads
```http
POST /campaign/GetLeads
```

**Request Body:**
```json
{
  "campaignId": "campaign-id",
  "offset": 0,
  "limit": 100
}
```

**Response:**
```json
{
  "items": [
    {
      "id": "lead-id",
      "linkedInUrl": "https://linkedin.com/in/username",
      "firstName": "John",
      "lastName": "Doe",
      "status": "CONTACTED"
    }
  ],
  "totalCount": 100
}
```

---

### Conversations

#### Get Conversations
```http
POST /conversation/GetAll
```

**Request Body:**
```json
{
  "offset": 0,
  "limit": 100,
  "campaignId": "optional-campaign-id"
}
```

---

### LinkedIn Accounts

#### List All Accounts
```http
POST /li_account/GetAll
```

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "items": [
    {
      "id": "account-id",
      "name": "Account Name",
      "linkedInUrl": "https://linkedin.com/in/myprofile",
      "status": "CONNECTED"
    }
  ],
  "totalCount": 2
}
```

---

### Lists

#### List All Lists
```http
POST /list/GetAll
```

**Request Body:**
```json
{
  "offset": 0,
  "limit": 100
}
```

**Response:**
```json
{
  "items": [
    {
      "id": "list-id",
      "name": "My Lead List",
      "leadCount": 250
    }
  ],
  "totalCount": 5
}
```

---

#### Create Empty List
```http
POST /list/CreateEmpty
```

**Request Body:**
```json
{
  "name": "New Lead List"
}
```

---

### Analytics

#### Get Overall Stats
```http
POST /analytics/GetOverallStats
```

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "totalCampaigns": 10,
  "activeCampaigns": 5,
  "totalLeads": 1000,
  "contactedLeads": 500,
  "repliedLeads": 50,
  "connectionRate": 45.5,
  "replyRate": 10.0
}
```

---

#### Get Campaign Stats
```http
POST /analytics/GetCampaignStats
```

**Request Body:**
```json
{
  "campaignId": "campaign-id"
}
```

**Response:**
```json
{
  "campaignId": "campaign-id",
  "totalLeads": 100,
  "contacted": 80,
  "replied": 15,
  "connectionRequests": 50,
  "connectionsAccepted": 40,
  "messagesSent": 200,
  "replyRate": 18.75
}
```

---

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 405 | Method Not Allowed - Wrong HTTP method |
| 429 | Rate Limited - Too many requests |
| 500 | Server Error - Try again later |

---

## Pagination

Most list endpoints support pagination:

```json
{
  "offset": 0,
  "limit": 100
}
```

- `offset`: Number of items to skip (default: 0)
- `limit`: Maximum items to return (default: 100, max: 100)

**Response includes:**
```json
{
  "items": [...],
  "totalCount": 500
}
```

---

**API Docs**: https://documenter.getpostman.com/view/23808049/2sA2xb5F75
**Version**: 1.1
**Updated**: 2025-12-19
