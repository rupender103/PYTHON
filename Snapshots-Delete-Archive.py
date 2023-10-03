import boto3

def lambda_handler(event, context):
    # Initialize AWS clients
    ec2 = boto3.client('ec2')

    # Retrieve all snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])
    snapshots = response['Snapshots']
    
    # Initialize lists to store snapshots
    snapshots_to_be_archived = []
    snapshots_deleted = []
    snapshots_in_use = []
    
    total_deleted_snapshots_size = 0

    # Iterate through each snapshot
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot['VolumeId']
        snapshot_size = snapshot['VolumeSize']
        tags = snapshot.get('Tags', [])
        
        # Check if the snapshot name contains "CV_CBT_Snap"
        if any(tag.get('Key') == 'Name' and tag.get('Value') == 'CV_CBT_Snap' for tag in tags):
            continue
        
        # Check if the snapshot is used by an AMI
        images = ec2.describe_images(Filters=[{'Name': 'block-device-mapping.snapshot-id', 'Values': [snapshot_id]}])['Images']
        if images:
            for image in images:
                ami_id = image['ImageId']
                snapshots_in_use.append({'snapshot_id': snapshot['SnapshotId'], 'ami_id': ami_id})
            continue

        # Check if the volume exists
        try:
            ec2.describe_volumes(VolumeIds=[volume_id])
        except ec2.exceptions.ClientError as e:
            # Skip deleting snapshot if the volume doesn't exist
            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                tags = [{'Key': 'Volume', 'Value': 'DoesNotExist'}]
                ec2.create_tags(Resources=[snapshot_id], Tags=tags)
                snapshots_to_be_archived.append(snapshot['SnapshotId'])
                continue
            
        else:
            ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            snapshots_deleted.append({'snapshot_id': snapshot['SnapshotId'], 'snapshot_size': snapshot['VolumeSize']})
            total_deleted_snapshots_size += snapshot['VolumeSize']
        
    response = {
        'statusCode': 200,
        'snapshots_to_be_archived': snapshots_to_be_archived,
        'snapshots_deleted': snapshots_deleted,
        'snapshots_in_use': snapshots_in_use
    }
    
    print("Total Deleted Snapshot Size:",total_deleted_snapshots_size)
    
    return response
