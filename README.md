# Air ifpshare converter

**ifpshare-converter** is a web application built with Flask that automates the conversion of documents from air ifpshare to PDF format.

## Technologies Used

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [reportlab](https://www.reportlab.com/)
- [HTML/CSS/JavaScript](https://www.w3schools.com/)

## Installation

To set up the **ifpshare-converter** application locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/KMChris/ifpshare-converter.git
   cd ifpshare-converter
   ```

2.  **Create a virtual environment**:

    ``` bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:

    -   On Windows:

        ``` bash
        venv\Scripts\activate
        ```

    -   On macOS/Linux:

        ``` bash
        source venv/bin/activate
        ```

4.  **Install the required packages**:

    ``` bash
    pip install -r requirements.txt
    ```

5.  **Run the application**:

    ``` bash
    python app.py
    ```

    The application will be accessible at `http://127.0.0.1:5000`.

## Usage

1.  Open your web browser and go to `http://127.0.0.1:5000`.
2.  Paste the link to the air ifpshare document you want to convert.
3.  Click on the "Download PDF" button.
4.  Once the conversion is complete, your PDF file will be downloaded automatically.

## Contributing

We welcome contributions to the **ifpshare-converter** project! To contribute:

1.  Fork the repository.
2.  Create a new branch: `git checkout -b feature/YourFeature`.
3.  Make your changes and commit them: `git commit -m 'Add new feature'`.
4.  Push to the branch: `git push origin feature/YourFeature`.
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
