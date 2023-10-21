import os

import pandas as pd
from dotenv import load_dotenv
from google.cloud import storage
from tqdm import tqdm  # Import tqdm

load_dotenv()


def get_content_type(blob):
    # Get the content type (media type) of the blob from its metadata
    return blob.content_type or "Unknown"


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
        content_type = get_content_type(blob)  # Get content type from metadata
        blob_info.append(
            {
                "Name": blob.name,
                "Size": blob.size,
                "Updated": blob.updated,
                "Content Type": content_type,
            }
        )

    # Create a DataFrame from blob_info list
    dfs = pd.DataFrame(blob_info)

    # Calculate summary stats for sizes
    size_stats = dfs["Size"].describe()
    print(size_stats)

    # Group by folders
    dfs["Folder"] = dfs["Name"].apply(lambda x: x.split("/")[0])
    folder_groups = dfs.groupby("Folder")

    # Add an extra layer for content type analysis under folder level
    with open("results.csv", "w") as file:
        size_stats.to_csv(file, header=["Size Statistics"])
        file.write("\n")

        for name, group in folder_groups:
            file.write(f"Folder: {name}\n")
            group["Size"].describe().to_csv(file, header=["Folder Size Statistics"])
            file.write("\n")

            # Group by content types within the folder
            content_type_groups = group.groupby("Content Type")
            for content_type, content_type_group in content_type_groups:
                file.write(f"Content Type: {content_type}\n")
                content_type_group["Size"].describe().to_csv(
                    file, header=["Content Type Size Statistics"]
                )
                file.write("\n")


if __name__ == "__main__":
    main()
