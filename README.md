# Google Cloud Storage Data Analyzer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project provides a Python library for analyzing data stored in Google Cloud Storage. It includes tools for calculating statistics on file sizes, content types, and more.

## Getting Started

To use this library, you'll need to set up a Google Cloud Storage account and create a `gcp_credential.json` file with your credentials. Here's how to get started:

1. Create a Google Cloud Storage account if you haven't already done so.
2. Create a new project in the Google Cloud Console.
3. Enable the Google Cloud Storage API for your project.
4. Create a service account or use your personal account to access the bucket.
5. Download the `gcp_credential.json` file for your service account or personal account.
6. Place the `gcp_credential.json` file in the `internal/configuration` directory of this project.

## Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your changes.
3. Make your changes and commit them to your branch.
4. Push your changes to your forked repository.
5. Open a pull request to merge your changes into the main repository.

Please make sure to include a detailed description of your changes in your pull request. We also recommend running the tests and linting tools before submitting your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.