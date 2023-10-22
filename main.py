import os

import pandas as pd
from dotenv import load_dotenv
from google.cloud import storage
from tqdm import tqdm  # Import tqdm

load_dotenv()


def main():
    project_id = os.getenv("GCP_PROJECT_ID")
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    credentials_path = os.getenv("GCP_CREDENTIAL_FILE_LOCATION")

    # Initialize client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    storage_client = storage.Client(project=project_id)

    # Get bucket
    bucket = storage_client.bucket(bucket_name)

    # Initialize an empty list to store blob info
    blob_info = []

    # Get list of objects in the bucket with tqdm
    for blob in tqdm(bucket.list_blobs(), desc="Processing files"):
        blob_info.append(
            {
                "Name": blob.name,
                "Size": blob.size,
                "Updated": blob.updated,
                "Content Type": blob.content_type,
            }
        )

    # Create a DataFrame from blob_info list
    dfs = pd.DataFrame(blob_info)

    # Initialize lists to store stats
    overall_stats = []
    folder_stats = []
    content_type_stats = []

    # Get blobs as before

    # Calculate overall bucket stats
    overall_stats.append(dfs["Size"].describe().to_dict())

    # Group by folders
    dfs["Folder"] = dfs["Name"].apply(lambda x: x.split("/")[0])
    folder_groups = dfs.groupby("Folder")

    # Group by folder
    for name, group in folder_groups:
        folder_stats.append({"Folder": name, **group["Size"].describe().to_dict()})

        # Group by content types within the folder
        content_type_groups = group.groupby("Content Type")
        for content_type, content_type_group in content_type_groups:
            content_type_stats.append(
                {
                    "Folder": name,
                    "Content Type": content_type,
                    **content_type_group["Size"].describe().to_dict(),
                }
            )

    # Write stats to CSV
    pd.DataFrame(overall_stats).to_csv("bucket_stats.csv", index=False)
    pd.DataFrame(folder_stats).to_csv("folder_stats.csv", index=False)
    pd.DataFrame(content_type_stats).to_csv("content_type_stats.csv", index=False)


if __name__ == "__main__":
    main()
