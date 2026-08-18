# ZPA Application Segment Manager

This script provides a command-line interface (CLI) to manage Zscaler Private Access (ZPA) Application Segments. It utilizes the `zscaler-python-client` library to interact with the Zscaler API, allowing you to list existing segments, create new segments, and update existing ones by adding Fully Qualified Domain Names (FQDNs).

## Features

-   **List Application Segments**: View all configured Application Segments in your ZPA tenant.
-   **Add Application Segments**: Create a new Application Segment with specified FQDNs, a segment group, and server groups.
-   **Update Application Segments**: Add new FQDNs or wildcards to an existing Application Segment.
-   **Verbose Logging**: Enable detailed logging for debugging purposes.

## Disclaimer

This project and script are provided "as is", without warranty of any kind, express or implied. The author is not responsible for any damage, data loss, or consequences resulting from the use of this script. You are solely responsible for how you use this tool and for verifying any changes it makes to your environment.

## Architecture Overview

In Zscaler Private Access (ZPA), the hierarchy for Application Segments is structured as follows:

```text
[ App Segment Group ]
          │
          ├────────► [ App Segment 1 ] ────────► [ Server Group A ]
          │                                  └─► [ Server Group B ]
          │
          ├────────► [ App Segment 2 ] ────────► [ Server Group C ]
          │
          └────────► [ App Segment N ] ────────► [ Server Group N ]
```
- **App Segment Group**: A logical grouping of one or more Application Segments.
- **App Segment**: Represents the application itself, defined by FQDNs or IP addresses.
- **Server Group**: A group of servers where the application is hosted. An App Segment can be tied to multiple Server Groups.

## Prerequisites

-   Python 3.6+
-   A ZPA tenant.
-   ZPA API Credentials with permissions to read and write Application Segments. For instructions on creating these, refer to the [Zscaler API Getting Started Guide](https://automate.zscaler.com/docs/getting-started/getting-started). Note that when [adding an API client](https://help.zscaler.com/authentication-service/adding-api-client), you must choose the **Secret** authentication method for this script. You will need:
    -   `Client ID`
    -   `Client Secret`
    -   `Customer ID` (AKA ZPA Account ID)
    -   `Vanity Domain` (e.g., `api.private.zscaler.com`)

## Setup and Installation

Follow these steps to set up the script and its environment.

### 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/bonzi316/zpa-app-segment-manager.git
cd zpa-app-segment-manager
```
### Project Structure

```
.
├── app-segment.py      # The main script provided
├── utils/
│   ├── __init__.py
│   ├── utils.py        # Helper for loading env vars, etc.
│   └── zpa.py          # Helper for ZPA API calls
├── requirements.txt
└── .env
```

### 3. Install Dependencies

# Create a virtual environment
```
python3 -m venv venv
```

# Activate the virtual environment
# On macOS/Linux:
```source venv/bin/activate```
# On Windows:
```.\venv\Scripts\activate```

# Install the required packages
```pip install -r requirements.txt```


### 4. Configure Environment Variables

The script loads API credentials and configuration from a `.env` file. Create a file named `.env` in the root of your project directory.

**Do not commit the `.env` file to version control.**

Copy the example below into your `.env` file and replace the placeholder values with your actual ZPA API credentials.

**`.env`**
```ini
# Zscaler API Configuration
# Replace with your actual ZPA API credentials

# The Client ID from your ZPA API key
export ZSCALER_CLIENT_ID="YOUR_API_CLIENT_ID"

# The Client Secret from your ZPA API key
export ZSCALER_CLIENT_SECRET="YOUR_API_SECRET"

# Your Zscaler vanity domain (e.g., api.private.zscaler.com)
export ZSCALER_VANITY_DOMAIN="ZSLOGIN DOMAIN"

# Your ZPA Customer ID (or use ZSCALER_CUSTOMER_ID)
export ZPA_CUSTOMER_ID="YOUR_ZPA_INSTANCE_ID"

# Your ZPA Env Type
export ZPA_CLOUD="PRODUCTION"
```

## Usage

The script is controlled via command-line arguments. The primary argument is `--action`, which determines what the script will do.

**Basic Syntax:**

```
python app-segment.py --action <ACTION> [OPTIONS]
```

**Actions and Arguments**

| Argument                     | Short | Description                                                                | Required For      |
| ---------------------------- | ----- | -------------------------------------------------------------------------- | ----------------- |
| `--action`                   | `-a`  | The action to perform. Choices: `list`, `list_segment_groups`, `list_server_groups`, `add`, `update`, `update_remove`.  | **Always**        |
| `--application-segment-id`   | `-asid` | The unique ID of the Application Segment to update or remove from.           | `update`, `update_remove` |
| `--segment-name`             | `-sn` | The name for a new Application Segment.                                    | `add`             |
| `--fqdns`                    | `-f`  | One or more FQDNs or wildcards to define the application (e.g., `app.domain.com` `*.cdn.com`). | `add`, `update`, `update_remove` |
| `--segment-group-id`         | `-sid`  | The ID of the Segment Group to associate the new segment with.               | `add`             |
| `--server-group-ids`         | `-sgid` | One or more Server Group IDs where the application is hosted.                | `add`             |
| `--verbose`                  | `-v`  | Enable verbose logging for debugging.                                      | *Optional*        |
| `--env`                      | `-e`  | Path to a custom `.env` file (e.g., `.env.custom_env`). If omitted, defaults to `.env`. | *Optional*        |

## Examples

**1. List all Application Segments**
```bash
python app-segment.py -a list
```
*(With a custom .env file)*
```bash
python app-segment.py -a list -e .env.custom_env
```

**2. List Segment Groups (Helper)**
```bash
python app-segment.py -a list_segment_groups
```

**3. List Server Groups (Helper)**
```bash
python app-segment.py -a list_server_groups
```

**4. Add a new Application Segment**
```bash
python app-segment.py -a add -sn "My New App" -f app1.domain.com app2.domain.com -sid 123456789 -sgid 987654321
```

**5. Update an existing Application Segment (Add FQDNs)**
```bash
python app-segment.py -a update -asid 1122334455 --fqdns new.app.com another.app.com
```

**6. Remove FQDNs from an existing Application Segment**
```bash
python app-segment.py -a update_remove -asid 1122334455 --fqdns old.app.com
```
