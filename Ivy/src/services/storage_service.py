import boto3
from botocore.exceptions import ClientError
from typing import BinaryIO, Dict, List
import os
from datetime import datetime, timedelta

class StorageService:
    def __init__(self, aws_access_key_id: str = None, 
                 aws_secret_access_key: str = None,
                 region_name: str = None,
                 bucket_name: str = None):
        self.aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        self.region_name = region_name or os.getenv('AWS_REGION', 'us-east-1')
        self.bucket_name = bucket_name or os.getenv('S3_BUCKET_NAME')

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def upload_file(self, file_obj: BinaryIO, file_name: str, 
                   content_type: str = None) -> Dict:
        """
        Upload a file to S3
        """
        try:
            extra_args = {'ContentType': content_type} if content_type else {}
            
            # Generate a unique file path using timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = f"uploads/{timestamp}_{file_name}"
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_path,
                ExtraArgs=extra_args
            )

            # Generate a presigned URL for temporary access
            url = self.generate_presigned_url(file_path)

            return {
                'file_path': file_path,
                'url': url,
                'bucket': self.bucket_name
            }

        except ClientError as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def download_file(self, file_path: str) -> BinaryIO:
        """
        Download a file from S3
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return response['Body']

        except ClientError as e:
            raise Exception(f"Failed to download file: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from S3
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True

        except ClientError as e:
            raise Exception(f"Failed to delete file: {str(e)}")

    def list_files(self, prefix: str = None) -> List[Dict]:
        """
        List files in the S3 bucket
        """
        try:
            if prefix:
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=prefix
                )
            else:
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name
                )

            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'url': self.generate_presigned_url(obj['Key'])
                })

            return files

        except ClientError as e:
            raise Exception(f"Failed to list files: {str(e)}")

    def generate_presigned_url(self, file_path: str, 
                             expiration: int = 3600) -> str:
        """
        Generate a presigned URL for temporary file access
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=expiration
            )
            return url

        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def copy_file(self, source_path: str, destination_path: str) -> Dict:
        """
        Copy a file within the same bucket
        """
        try:
            self.s3_client.copy_object(
                Bucket=self.bucket_name,
                CopySource={'Bucket': self.bucket_name, 'Key': source_path},
                Key=destination_path
            )

            return {
                'source': source_path,
                'destination': destination_path,
                'url': self.generate_presigned_url(destination_path)
            }

        except ClientError as e:
            raise Exception(f"Failed to copy file: {str(e)}")

    def get_file_metadata(self, file_path: str) -> Dict:
        """
        Get metadata for a specific file
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )

            return {
                'content_type': response.get('ContentType'),
                'content_length': response.get('ContentLength'),
                'last_modified': response.get('LastModified').isoformat(),
                'metadata': response.get('Metadata', {})
            }

        except ClientError as e:
            raise Exception(f"Failed to get file metadata: {str(e)}") 