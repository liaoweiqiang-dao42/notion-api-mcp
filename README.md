# Notion API MCP

A Model Context Protocol (MCP) server that provides advanced todo list management and content organization capabilities through Notion's API.

## Getting Started

### 1. Create a Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name your integration (e.g., "My MCP Integration")
4. Select the workspace where you'll use the integration
5. Copy the "Internal Integration Token" - this will be your `NOTION_API_KEY`
   - Should start with "ntn_"

### 2. Set Up Notion Access

You'll need either a parent page (for creating new databases) or an existing database ID:

#### Option A: Parent Page for New Databases
1. Open Notion in your browser
2. Create a new page or open an existing one where you want to create databases
3. Click the ••• menu in the top right
4. Select "Add connections" and choose your integration
5. Copy the page ID from the URL - it's the string after the last slash and before the question mark
   - Example: In `https://notion.so/myworkspace/123456abcdef...`, the ID is `123456abcdef...`
   - This will be your `NOTION_PARENT_PAGE_ID`

#### Option B: Existing Database
1. Open your existing Notion database
2. Make sure it's connected to your integration (••• menu > Add connections)
3. Copy the database ID from the URL
   - Example: In `https://notion.so/myworkspace/123456abcdef...?v=...`, the ID is `123456abcdef...`
   - This will be your `NOTION_DATABASE_ID`

### 3. Install the MCP Server

1. Create virtual environment:
```bash
cd notion-api-mcp
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv pip install -e .
```

3. Configure environment:
```bash
cp .env.integration.template .env
```

4. Edit .env with your Notion credentials:
```env
NOTION_API_KEY=ntn_your_integration_token_here

# Choose one or both of these depending on your needs:
NOTION_PARENT_PAGE_ID=your_page_id_here  # For creating new databases
NOTION_DATABASE_ID=your_database_id_here  # For working with existing databases
```

### 4. Configure Claude Desktop

IMPORTANT: While the server supports both .env files and environment variables, Claude Desktop specifically requires configuration in its config file to use the MCP.

Add to Claude Desktop's config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "notion-api": {
      "command": "/path/to/your/.venv/bin/python",
      "args": ["-m", "notion_api_mcp"],
      "env": {
        "NOTION_API_KEY": "ntn_your_integration_token_here",
        
        // Choose one or both:
        "NOTION_PARENT_PAGE_ID": "your_page_id_here",
        "NOTION_DATABASE_ID": "your_database_id_here"
      }
    }
  }
}
```

Note: Even if you have a .env file configured, you must add these environment variables to the Claude Desktop config for Claude to use the MCP. The .env file is primarily for local development and testing.

## Configuration Details

### Environment Variables

The server supports configuration through both a .env file and system environment variables. When both are present, system environment variables (including those set in the Claude Desktop MCP config) take precedence over .env file values.

Required:
- `NOTION_API_KEY`: Your Notion API integration token
  - Must start with "ntn_"
  - Get from https://www.notion.so/my-integrations

Optional (at least one is required):
- `NOTION_PARENT_PAGE_ID`: ID of a Notion page where you want to create new databases
  - Must be a page that has granted access to your integration
  - Required if you want to create new databases
  - Get from the page's URL

- `NOTION_DATABASE_ID`: ID of an existing database
  - Must be a database that has granted access to your integration
  - Required if you want to work with an existing database
  - Get from the database's URL

### Configuration Sources

You can provide these variables in two ways:

1. Environment File (.env):
```env
NOTION_API_KEY=ntn_your_integration_token_here
NOTION_PARENT_PAGE_ID=your_page_id_here
NOTION_DATABASE_ID=your_database_id_here
```

2. Claude Desktop MCP Config:
```json
{
  "mcpServers": {
    "notion-api": {
      "command": "/path/to/your/.venv/bin/python",
      "args": ["-m", "notion_api_mcp"],
      "env": {
        "NOTION_API_KEY": "ntn_your_integration_token_here",
        "NOTION_PARENT_PAGE_ID": "your_page_id_here",
        "NOTION_DATABASE_ID": "your_database_id_here"
      }
    }
  }
}
```

The server will:
1. First load any values from your .env file
2. Then apply any system environment variables (including those from MCP config)
3. System environment variables take precedence over .env values

This means you can:
- Use .env for local development and testing
- Override values via MCP config for production use
- Mix and match sources (e.g., some values in .env, others in MCP config)

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Overview of available tools and usage examples
- [API Reference](docs/api_reference.md) - Detailed API endpoints and implementation details
- [Test Coverage Matrix](docs/test_coverage_matrix.md) - Test coverage and validation status
- [Dependencies](docs/dependencies.md) - Project dependencies and version information
- [Changelog](docs/CHANGELOG.md) - Development progress and updates

## Features

### Core Functionality
- Clean async implementation using httpx
- Type-safe configuration using Pydantic
- Simple configuration via environment variables
- Comprehensive error handling
- Resource cleanup and connection management

### Database Operations

The create_database tool allows you to create new databases in Notion. Important notes:
- The parent must be a Notion page that has granted access to your integration
- Currently, databases can only be created as children of Notion pages or wiki databases (Notion API limitation)
- Once created, databases cannot be moved to a different parent

Example database creation:
```python
{
  "parent_page_id": "your_page_id",
  "title": "My Tasks",
  "properties": {
    "Name": {"title": {}},
    "Status": {
      "select": {
        "options": [
          {"name": "Not Started", "color": "red"},
          {"name": "In Progress", "color": "yellow"},
          {"name": "Done", "color": "green"}
        ]
      }
    }
  }
}
```

Other database features:
- Dynamic property types including select, multi-select, date, number, formula
- Advanced filtering with multiple conditions (AND/OR logic)
- Rich sorting options combining multiple properties
- Smart pagination for efficient data access
- Powerful search across all content

### Todo Management
- Rich text descriptions with full Markdown and inline code support
- Flexible due dates with timezone-aware scheduling and reminders
- Customizable priority levels (high/medium/low) with visual indicators
- Dynamic status tracking (Not Started, In Progress, Completed, etc.)
- Hierarchical categories and multiple tags for powerful organization
- Collaborative task notes and threaded comments
- Nested subtasks with independent progress tracking
- Database templates for recurring task patterns (Note: Template blocks deprecated as of March 27, 2023)

### Content Management
- Rich text formatting with support for headings, quotes, callouts, and code blocks
- Structured block operations for content organization
- Smart link previews and embeds
- Hierarchical list management
- Advanced block features including synced blocks and database views

## Project Structure

```
notion-api-mcp/
├── src/
│   └── notion_api_mcp/
│       ├── __init__.py
│       ├── server.py           # Main MCP server
│       ├── api/               # API interaction modules
│       │   ├── __init__.py
│       │   ├── blocks.py     # Block operations
│       │   ├── databases.py  # Database operations
│       │   └── pages.py      # Page operations
│       ├── models/           # Data models
│       │   ├── __init__.py
│       │   ├── properties.py # Property definitions
│       │   └── responses.py  # API responses
│       └── utils/            # Utilities
│           ├── __init__.py
│           ├── auth.py       # Authentication
│           └── formatting.py # Text formatting
├── tests/                    # Test directory
├── docs/                     # Documentation
└── examples/                 # Example scripts
```

## Development

The server uses modern Python async features throughout:
- Type-safe configuration using Pydantic models
- Async HTTP using httpx for better performance
- Clean MCP integration for exposing Notion capabilities
- Proper resource cleanup and error handling

### Debugging

The server includes comprehensive logging:
- Console output for development
- File logging when running as a service
- Detailed error messages
- Request/response logging at debug level

Set `PYTHONPATH` to include the project root when running directly:

```bash
PYTHONPATH=/path/to/project python -m notion_api_mcp
```

## Future Development

Planned enhancements:
1. Performance Optimization
   - Add request caching
   - Optimize database queries
   - Implement connection pooling

2. Advanced Features
   - Multi-workspace support
   - Batch operations
   - Real-time updates
   - Advanced search capabilities

3. Developer Experience
   - Interactive API documentation
   - CLI tools for common operations
   - Additional code examples
   - Performance monitoring

4. Testing Enhancements
   - Performance benchmarks
   - Load testing
   - Additional edge cases
   - Extended integration tests