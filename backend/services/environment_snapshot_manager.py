"""
EnvironmentSnapshotManager: Save and restore VM/browser/workspace state (local & GCloud)
"""
import os
import tarfile
import shutil
from datetime import datetime
from pathlib import Path
import logging

try:
    from google.cloud import storage
    GCLOUD_AVAILABLE = True
except ImportError:
    GCLOUD_AVAILABLE = False

logger = logging.getLogger("EnvSnapshot")

class EnvironmentSnapshotManager:
    def __init__(self, local_dir="backend/data/env_snapshots", gcloud_bucket=None, gcloud_creds=None):
        self.local_dir = Path(local_dir)
        self.gcloud_bucket = gcloud_bucket or os.getenv("GCLOUD_SNAPSHOT_BUCKET")
        self.gcloud_creds = gcloud_creds or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.local_dir.mkdir(parents=True, exist_ok=True)
        if GCLOUD_AVAILABLE and self.gcloud_bucket:
            self.gcloud_client = storage.Client.from_service_account_json(self.gcloud_creds) if self.gcloud_creds else storage.Client()
            self.bucket = self.gcloud_client.bucket(self.gcloud_bucket)
        else:
            self.gcloud_client = None
            self.bucket = None

    def save_snapshot(self, session_id, src_path, to_cloud=False):
        """Archive src_path and save locally or to GCloud"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_name = f"{session_id}_{timestamp}.tar.gz"
        archive_path = self.local_dir / archive_name
        # Create tar.gz archive
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(src_path, arcname=os.path.basename(src_path))
        logger.info(f"Snapshot saved locally: {archive_path}")
        if to_cloud and self.bucket:
            blob = self.bucket.blob(archive_name)
            blob.upload_from_filename(str(archive_path))
            logger.info(f"Snapshot uploaded to GCloud: {archive_name}")
            return f"gcloud://{self.gcloud_bucket}/{archive_name}"
        return str(archive_path)

    def restore_snapshot(self, session_id, archive_name, from_cloud=False):
        """Restore archive locally or from GCloud"""
        archive_path = self.local_dir / archive_name
        if from_cloud and self.bucket:
            blob = self.bucket.blob(archive_name)
            blob.download_to_filename(str(archive_path))
            logger.info(f"Snapshot downloaded from GCloud: {archive_name}")
        # Extract archive
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=self.local_dir / f"restored_{session_id}")
        logger.info(f"Snapshot restored to: {self.local_dir / f'restored_{session_id}' }")
        return str(self.local_dir / f"restored_{session_id}")
