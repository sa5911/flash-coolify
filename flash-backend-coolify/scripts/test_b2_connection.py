"""
Quick test script to verify Backblaze B2 connection.
Run this locally to test your B2 credentials before deploying.
"""

import boto3
from botocore.exceptions import ClientError

# Your B2 credentials
B2_KEY_ID = "005840bd883f2c00000000001"
B2_APPLICATION_KEY = "K005yWC9Xm4+PemwdO2GB06smKEcUpw"
B2_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com"
B2_REGION = "us-east-005"

# YOU NEED TO SET THIS - What is your bucket name?
B2_BUCKET_NAME = "flash-erp"

def test_connection():
    print("Testing Backblaze B2 connection...")
    print(f"Endpoint: {B2_ENDPOINT_URL}")
    print(f"Region: {B2_REGION}")
    print(f"Bucket: {B2_BUCKET_NAME}")
    print()
    
    try:
        client = boto3.client(
            "s3",
            endpoint_url=B2_ENDPOINT_URL,
            aws_access_key_id=B2_KEY_ID,
            aws_secret_access_key=B2_APPLICATION_KEY,
            region_name=B2_REGION,
        )
        
        # Test listing buckets
        print("1. Listing buckets...")
        response = client.list_buckets()
        buckets = [b["Name"] for b in response.get("Buckets", [])]
        print(f"   Found buckets: {buckets}")
        
        if B2_BUCKET_NAME == "YOUR_BUCKET_NAME_HERE":
            print("\n⚠️  Please set B2_BUCKET_NAME to your actual bucket name!")
            return
        
        # Test uploading a file
        print(f"\n2. Testing upload to {B2_BUCKET_NAME}...")
        test_key = "test/connection_test.txt"
        test_content = b"Hello from Flash ERP! This is a connection test."
        
        client.put_object(
            Bucket=B2_BUCKET_NAME,
            Key=test_key,
            Body=test_content,
            ContentType="text/plain",
        )
        print(f"   ✅ Successfully uploaded: {test_key}")
        
        # Get the public URL
        public_url = f"https://f005.backblazeb2.com/file/{B2_BUCKET_NAME}/{test_key}"
        print(f"   Public URL: {public_url}")
        
        # Clean up test file
        print("\n3. Cleaning up test file...")
        client.delete_object(Bucket=B2_BUCKET_NAME, Key=test_key)
        print("   ✅ Test file deleted")
        
        print("\n✅ All tests passed! B2 connection is working.")
        
    except ClientError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()
