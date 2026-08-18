from zscaler import ZscalerClient
import traceback
from pprint import pprint

def add_pac_file(client: ZscalerClient, name: str, domain: str, pac_content: str):
    try:
        validation,raw,err = client.zia.pac_files.validate_pac_file(pac_file_content=pac_content)

        if (err):
            print(f'Error in pacfile validation {err}')
        print(err)
        pprint(validation)
        pprint(raw)
        exit(1)

        pac_file,_,err = client.zia.pac_files.add_pac_file(
                    name=name,
                    description="Added via Script",
                    domain=domain,
                    pac_commit_message="Added via Script",
                    pac_version_status="DEPLOYED",
                    pac_content=pac_content)

        if err:
            print(err)
            raise Exception(err)

        pprint(pac_file)    
        return pac_file
    
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f"Error adding pac file: {str(e)}")

# Function to fetch details of a specific URL category
def get_url_category_details(client: ZscalerClient, category_name):
    try:
        # List all URL categories
        
        url_categories,_,err =  client.zia.url_categories.list_categories()
        if err:
            print(err)
            return None
        for category in url_categories:
            #print(category["id"])
            if ( not category["custom_category"]):
                #print(f"Skip pre-defined Category {category['id']}")
                continue

            #pprint(category.as_dict())
            #print("************")
            if category["configured_name"].lower() == category_name.lower():
                return category
        raise ValueError(f"URL category '{category_name}' not found.")
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f"Error fetching URL category details: {str(e)}")

# Function to segregate URLs by their types
def segregate_urls_by_type(url_category):
    return {
        key: value
        for key, value in {
            "keywords": url_category["keywords"],
            "keywords retaining parent category": url_category["keywords_retaining_parent_category"],
            "custom urls": url_category["urls"],
            "urls retaining parent category": url_category["db_categorized_urls"],
        }.items()
        if value
    }



# Function: Create URL Category
def create_url_category(client: ZscalerClient, category_name, description, urls=None, keywords=None):
    try:
        urls = urls or []
        keywords = keywords or []
                                 
        new_category, _, error = client.zia.url_categories.add_url_category(
            configured_name=category_name,
            super_category="USER_DEFINED",
            description=description,
            urls=urls,
            keywords=keywords,
        )

        if error:
            print(f"Error creating URL category: {error}")
            return None

        print(f"URL Category created successfully: {new_category.as_dict()}")
        return new_category

    except Exception as e:
        print(f"Failed to create URL category: {e}")
        return None

# Function: Create SSL Inspection Policy
def create_ssl_inspection_policy(client: ZscalerClient, policy_name, description, action, urls=None, rule_index=None):
    try:
        urls = urls or []

        new_policy, _, error = client.zia.ssl_inspection_rules.add_rule(
            name=policy_name,
            description=description,
            action=action,
            urls=urls,
            order=rule_index,
        )

        if error:
            print(f"Error creating SSL inspection policy: {error}")
            return None

        print(f"SSL Inspection Policy created successfully: {new_policy.as_dict()}")
        return new_policy

    except Exception as e:
        print(f"Failed to create SSL inspection policy: {e}")
        return None

# Function: Create Firewall Rule
def create_firewall_rule(client: ZscalerClient, rule_name, description, action, destinations=None, protocols=None, rule_index=None):
    try:
        destinations = destinations or []
        protocols = protocols or []

        
        new_rule, _, error = client.zia.cloud_firewall_rules.add_rule(
            name=rule_name,
            description=description,
            action=action,
            destinations=destinations,
            protocols=protocols,
            order=rule_index,
        )

        if error:
            print(f"Error creating firewall rule: {error}")
            return None

        print(f"Firewall Rule created successfully: {new_rule.as_dict()}")
        return new_rule

    except Exception as e:
        print(f"Failed to create firewall rule: {e}")
        return None

# Function: Create URL Filtering Policy
def create_url_filtering_policy(client:ZscalerClient, policy_name, description, urls, action, rule_index=None):
    try:
        new_policy, _, error = client.zia.url_filtering.add_rule(
            name=policy_name,
            description=description,
            urls=urls,
            action=action,
            order=rule_index,
        )

        if error:
            print(f"Error creating URL filtering policy: {error}")
            return None

        print(f"URL Filtering Policy created successfully: {new_policy.as_dict()}")
        return new_policy

    except Exception as e:
        print(f"Failed to create URL filtering policy: {e}")
        return None

# Function: List Rules or Policies
def list_items(client:ZscalerClient, item_type):
    try:
        if item_type == "SSL_POLICIES":
            policies,_,err = client.zia.ssl_inspection_rules.list_rules()
            for p in sorted(policies, key=lambda x: (x['order'] == -1, x['order'])):
                print(f"ID: {p['id']} - Order: {p['order']:3} - Action : {p['action']['type']:15} - Name: {p['name']:30}")
            #print(f"SSL Policies: {policies.as_dict()}")
            return policies

        elif item_type == "FIREWALL_RULES":
            policies,_,err =  client.zia.cloud_firewall_rules.list_rules()
            print(f"Firewall Rules: ")
            for p in sorted(policies, key=lambda x: (x['order'] == -1, x['order'])):
                #pprint(p)
                print(f"ID: {p['id']} - Order: {p['order']:3} - Action : {p['action']:15} - Name: {p['name']:30}")
            return policies

        elif item_type == "URL_FILTERING_POLICIES":
            policies,_,err = client.zia.url_filtering.list_rules()
            print(f"URL Filtering Policies: ")
            for p in sorted(policies, key=lambda x: (x['order'] == -1, x['order'])):
                #pprint(p.as_dict())
                print(f"ID: {p['id']} - Order: {p['order']:3} - Action : {p['action']:10} - Name: {p['name']:30}")
            return policies

        else:
            print(f"Invalid item type: {item_type}")
            return None
    except Exception as e:
        print(f"Failed to list items: {e}")
        return None

# Function: Move Rule to New Index
def move_rule(client, rule_id, new_index, rule_type):
    try:
        if rule_type == "SSL_POLICIES":
            client.zia.ssl.update_ssl_policy(rule_id, order=new_index)
            print(f"SSL policy {rule_id} moved to index {new_index}.")

        elif rule_type == "FIREWALL_RULES":
            client.zia.firewall.update_firewall_rule(rule_id, order=new_index)
            print(f"Firewall rule {rule_id} moved to index {new_index}.")

        elif rule_type == "URL_FILTERING_POLICIES":
            client.zia.url_filtering.update_filtering_policy(rule_id, order=new_index)
            print(f"URL filtering policy {rule_id} moved to index {new_index}.")

        else:
            print(f"Invalid rule type: {rule_type}")
            return None

    except Exception as e:
        print(f"Failed to move rule: {e}")
        return None
