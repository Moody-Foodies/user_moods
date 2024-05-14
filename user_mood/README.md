### user_moods_api
This document details the installation, usage, and contribution guidelines for the user_moods_api project.

## Installation
Clone the repository:

```Bash
git clone <repository_url>
```

Navigate to the project directory:

```Bash
cd user_moods_api
```

Install dependencies:

```Bash
pipenv install
```

## Running the Application
To run the Flask application locally, execute:

```Bash
./bootstrap.sh
```

## API Documentation

You can access the Swagger documentation for the API [here](/apidocs).


## Endpoints

`GET /moods`: Retrieves user moods.
`POST /moods`: Adds a new mood.

## Testing

The project uses pytest for testing. Run the tests with:

``` Bash
coverage run -m pytest 
```

## Contributing
We welcome contributions! Feel free to submit issues or pull requests.

## License
This project is licensed under the [MIT License](LICENSE).