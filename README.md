# MCP Cloud Run Sample - Google Store Mock

This project demonstrates how to deploy an MCP server to Google Cloud Run. This specific implementation mocks a Google Store API, providing data about phones, earbuds, watches, and more.

## Setup GCP Project

Configure your working project:
```bash
gcloud config set project [PROJECT_ID]
```

Enable required APIs:
```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

## Init project with uv

```sh
uv init --description "Example of deploying a Google Store Mock MCP server on Cloud Run" --bare --python 3.13
```

## Create service account

```sh
gcloud iam service-accounts create mcp-server-sa --display-name="MCP Server Service Account"
```

## server.py

The server uses `FastMCP` to define tools and resources for mocking Google Store data.

```python
import asyncio
import logging
import os
from typing import List, Dict, Any, Optional

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Google Store Mock Server 📱⌚🏠")

# Mock data for Google Store
STORE_PRODUCTS = [
    # Phones
    {
        "id": "p9pxl",
        "category": "phones",
        "name": "Pixel 9 Pro XL",
        "description": "The most powerful Pixel yet, with a pro-level camera and Gemini AI.",
        "price": 1099.00,
        "currency": "USD",
        "specs": ["6.8-inch Super Actua display", "Triple rear camera system", "Tensor G4 chip"]
    },
    # ... (see server.py for full data)
]

@mcp.tool()
def list_categories() -> List[str]:
    """Lists all available product categories in the Google Store."""
    # ...

@mcp.tool()
def get_products_by_category(category: str) -> List[Dict[str, Any]]:
    """Retrieves all products for a specific category."""
    # ...

@mcp.tool()
def get_product_details(product_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves detailed information about a specific product."""
    # ...

@mcp.tool()
def get_active_offers() -> List[Dict[str, Any]]:
    """Retrieves currently active offers and promotions."""
    # ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    asyncio.run(
        mcp.run_async(
            transport="streamable-http", 
            host="0.0.0.0", 
            port=port
        )
    )
```

## Package Installation

```sh
uv add fastmcp==2.12.4 --no-sync
```

## Deploy to Cloud Run

```sh
export GOOGLE_CLOUD_PROJECT=your-project-id

gcloud run deploy google-store-mcp-server \
    --service-account=mcp-server-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --no-allow-unauthenticated \
    --region=europe-west1 \
    --source=. \
    --labels=dev-tutorial=codelab-mcp
```

## Troubleshooting Local uv Issues

If you encounter issues with the `uv.lock` file referring to private registries:

```sh
# Delete the old lockfile
rm uv.lock

# Regenerate it forcing the public index
uv lock --default-index https://pypi.org/simple

# Authenticate for local development if needed
gcloud auth login
gcloud auth application-default login
uv pip install keyrings.google-artifactregistry-auth
export UV_KEYRING_PROVIDER=subprocess
```# mcp-cloudrun-gstore
