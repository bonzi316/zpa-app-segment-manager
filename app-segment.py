#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser
from dotenv import load_dotenv
from zscaler import ZscalerClient
from pprint import pprint

# Get the absolute path of the current script 
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level
project_root = os.path.dirname(script_dir)
# 3. Add this to to sys.path
sys.path.insert(0, project_root) 

from utils.utils import *
from utils.zpa import *


def main():
    # Setting up argparse for command-line arguments
    parser = ArgumentParser(description="Manage ZPA Application Segments via zscaler-python-client.")
    parser.add_argument("-a","--action", choices=["list", "list_segment_groups", "list_server_groups", "add","update", "update_remove"], required=True, help="Action to perform: 'list', 'list_segment_groups', 'list_server_groups', 'add', 'update', or 'update_remove'.")
    parser.add_argument("-asid","--application-segment-id", help="Application segment ID to update FQDNs.")
    parser.add_argument("-sn", "--segment-name", help="Name of the new application segment (required for creation).")
    parser.add_argument("-f","--fqdns", nargs="*", help="List of FQDNs to add.")
    parser.add_argument("-sid","--segment-group-id", help="Segment group ID (required for creation).")
    parser.add_argument("-sgid","--server-group-ids", nargs="*", help="List of server group IDs (required for creation).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging (default: disabled).")
    parser.add_argument("-e", "--env", help="Path to custom .env file", default=None)

    args = parser.parse_args()

    # Load environment variables
    try:
        env_vars = load_environment_variables(args.env)
        env_vars["logging"]["enabled"] = args.verbose
        env_vars["logging"]["verbose"] = args.verbose
        config = {
            "clientId": env_vars["clientId"],
            "clientSecret": env_vars["clientSecret"],
            "vanityDomain": env_vars["vanityDomain"],
            "customerId": env_vars.get("customerId"),
            "logging": env_vars["logging"],
        }
        client = ZscalerClient(config) 

    except ValueError as e:
        print(e)
        return

    # Perform action specified in command-line arguments
    if args.action == "list":
        list_application_segments(client)
    elif args.action == "list_segment_groups":
        list_segment_groups(client)
    elif args.action == "list_server_groups":
        list_server_groups(client)
    elif args.action == "update":
        if args.application_segment_id:
            add_fqdns_to_segment(client, application_segment_id=args.application_segment_id, fqdns=args.fqdns)
        else:
            print("Error: Missing required arguments for updating existing application segments: 'application_segment_id'.")
            return           
    elif args.action == "update_remove":
        if args.application_segment_id:
            remove_fqdns_from_segment(client, application_segment_id=args.application_segment_id, fqdns=args.fqdns)
        else:
            print("Error: Missing required arguments for removing FQDNs from application segments: 'application_segment_id'.")
            return           
    elif args.action == "add":
        if not args.segment_name or not args.segment_group_id or not args.server_group_ids:
            print("Error: Missing required arguments for creating new application segments: 'segment-name', 'segment-group-id', and 'server-group-ids'.")
            return
        add_fqdns_to_segment(
            client,
            segment_name=args.segment_name,
            fqdns=args.fqdns,
            segment_group_id=args.segment_group_id,
            server_group_ids=args.server_group_ids,
        )

if __name__ == "__main__":
    main()