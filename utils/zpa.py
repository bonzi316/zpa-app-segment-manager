
from pprint import pprint
from zscaler.exceptions import ZscalerAPIException

def list_application_segments(client):
    """
    Lists all application segments in the ZPA environment.

    :param client: Authenticated ZscalerClient instance.
    """
    try:
        app_segments, _, err = client.zpa.application_segment.list_segments()
        if not app_segments:
            print("No application segments found.")
            return

        print("Application Segments:")
        for segment in app_segments:
            #pprint(segment.as_dict())
            server_groups=[]
            for group in segment['server_groups']:
                server_groups.append(group['name'])
            print(f"# Name: {segment['name']} (ID: {segment['id']})")
            print(f"  - App Segment Group: {segment['segment_group_name']} (ID: {segment['segment_group_id']})")
            print(f"  - Server Group: {server_groups}")
            print(f"  - FQDNs")
            for fqdn in segment['domain_names']:
                print(f"    - {fqdn}")
            
            #print(f"ID: {segment['id']}, Name: {segment['name']}, Server Groups: {server_groups}, App Segment Group : {segment['segment_group_name']} ({segment['segment_group_id']})")
            #for fqdn in segment['domain_names']:
            #    print(f"  - {fqdn}")
    except Exception as e:
        print(f"Error while retrieving application segments: {e}")



def add_fqdns_to_segment(client, application_segment_id=None, segment_name=None, fqdns=None, segment_group_id=None, server_group_ids=None):
    """
    Adds FQDNs to an existing or new ZPA application segment.

    :param client: Authenticated ZscalerClient instance.
    :param application_segment_id: ID of the application segment to update (if updating).
    :param segment_name: Name of the segment (required for new segments).
    :param fqdns: List of FQDNs to add.
    :param segment_group_id: ID of the segment group (required for new segments).
    :param server_group_ids: List of server group IDs to bind (required for new segments).
    """
    if not fqdns or not isinstance(fqdns, list):
        print("Error: FQDNs must be a non-empty list.")
        return

    try:
        if application_segment_id:
            # Updating an existing application segment
            app_segment, _, err = client.zpa.application_segment.get_segment(segment_id=application_segment_id)
            if app_segment:
                app_segment['domain_names'].extend(fqdns)

                '''
                print(f"ID: {application_segment_id}")
                print(f"Name: {app_segment['name']}")
                print(f"Description: {app_segment['name']}")
                print(f"FQDN: {app_segment['domain_names']}")
                print(f"Group ID: {app_segment['segment_group_id']}")
                print(f"Ports: {app_segment['tcp_port_ranges']}")
                '''

                response,_,err = client.zpa.application_segment.update_segment(
                    segment_id=application_segment_id,
                    name=app_segment['name'],
                    description=app_segment['description'],
                    #enabled=True,
                    domain_names=app_segment['domain_names'],
                    segment_group_id=app_segment['segment_group_id'],
                    tcp_port_ranges=app_segment['tcp_port_ranges'],
                    udp_port_ranges=app_segment['udp_port_ranges'],
                    health_reporting=app_segment['health_reporting'],
                )
                if err:
                    print(f"Error: Update App Segment ID {application_segment_id} : {err}")

                print(f"Successfully updated application segment '{app_segment['name']}' with new FQDNs ({fqdns}).")
            else:
                print(f"Error: Application segment with ID {application_segment_id} not found.")
        else:
            # Creating a new application segment
            if not segment_name or not segment_group_id or not server_group_ids:
                print("Error: 'segment_name', 'segment_group_id', and 'server_group_ids' are required for creating new segments.")
                return

            new_segment = {
                "name": segment_name,
                "domainNames": fqdns,
                "enabled": True,
                "segmentGroupId": segment_group_id,
                "serverGroups": [{"id": server_id} for server_id in server_group_ids],
                "description": "Bulk FQDN addition using zscaler-python-client."
            }
            response, _, err = client.zpa.application_segment.add_segment(new_segment)
            print(f"Successfully created new application segment '{response['name']}' with ID {response['id']}.")
    except Exception as e:
        print(f"Error while managing application segments: {e}")



def remove_fqdns_from_segment(client, application_segment_id=None, fqdns=None):
    """
    Removes specific FQDNs from an existing ZPA application segment.

    :param client: Authenticated ZscalerClient instance.
    :param application_segment_id: ID of the application segment to update.
    :param fqdns: List of FQDNs to remove.
    """
    if not fqdns or not isinstance(fqdns, list):
        print("Error: FQDNs must be a non-empty list.")
        return

    try:
        if application_segment_id:
            # Updating an existing application segment
            app_segment, _, err = client.zpa.application_segment.get_segment(segment_id=application_segment_id)
            if app_segment:
                original_len = len(app_segment['domain_names'])
                # Remove fully matching FQDNs in-place
                for domain in fqdns:
                    if domain in app_segment['domain_names']:
                        app_segment['domain_names'].remove(domain)
                
                if len(app_segment['domain_names']) == original_len:
                    print(f"No matching FQDNs found to remove in segment '{app_segment['name']}'.")
                    return
                
                if len(app_segment['domain_names']) == 0:
                    print(f"Error: Cannot remove all FQDNs from the segment. A segment must have at least one FQDN.")
                    return

                response,_,err = client.zpa.application_segment.update_segment(
                    segment_id=application_segment_id,
                    name=app_segment['name'],
                    description=app_segment['description'],
                    domain_names=app_segment['domain_names'],
                    segment_group_id=app_segment['segment_group_id'],
                    tcp_port_ranges=app_segment['tcp_port_ranges'],
                    udp_port_ranges=app_segment['udp_port_ranges'],
                    health_reporting=app_segment['health_reporting'],
                )
                if err:
                    print(f"Error: Update App Segment ID {application_segment_id} : {err}")

                print(f"Successfully removed FQDNs ({fqdns}) from application segment '{app_segment['name']}'.")
            else:
                print(f"Error: Application segment with ID {application_segment_id} not found.")
        else:
            print("Error: 'application_segment_id' is required for removing FQDNs.")
    except Exception as e:
        print(f"Error while managing application segments: {e}")


def list_segment_groups(client):
    """
    Lists all segment groups in the ZPA environment.

    :param client: Authenticated ZscalerClient instance.
    """
    try:
        groups, _, err = client.zpa.segment_groups.list_groups()
        if not groups:
            print("No segment groups found.")
            return

        print("Segment Groups:")
        for group in groups:
            print(f" - {group['name']} (ID: {group['id']})")
    except Exception as e:
        print(f"Error while retrieving segment groups: {e}")


def list_server_groups(client):
    """
    Lists all server groups in the ZPA environment.

    :param client: Authenticated ZscalerClient instance.
    """
    try:
        groups, _, err = client.zpa.server_groups.list_groups()
        if not groups:
            print("No server groups found.")
            return

        print("Server Groups:")
        for group in groups:
            print(f" - {group['name']} (ID: {group['id']})")
    except Exception as e:
        print(f"Error while retrieving server groups: {e}")


def list_zpa_idps(client, verbose=True):
    """
    Retrieves all ZPA IDP associated with the customer.

    :param client: Authenticated ZscalerClient instance.
    :param verbose: Boolean flag for verbose logging.
    :return: List of IDP 
    """
    try:
        idps, raw, err = client.zpa.idp.list_idps()  # API call to list devices
        if err:
            print(err)
            exit(1)
        if verbose:
            print("Listing all IDP:")
            for idp in idps:
                #pprint(idp.as_dict())
                print(f"IDP ID: {idp['id']} - Name: {idp['name']:30s} - Enabled: {idp['enabled']} - Domains: {idp['domain_list']}")
                #print(f"Device ID: {device['hardware_fingerprint']}, Username: {device['user']}, State: {device['registration_state']}, "
                #      f"Hostname: {device['machine_hostname']}, OS: {device['os_version']}")
                #exit(1)
        return idps
    except ZscalerAPIException as e:
        raise RuntimeError(f"Error listing IDP : {e}")