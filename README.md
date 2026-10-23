# ScamSense — Your Personal Digital Safety Shield

## Overview

ScamSense is a Flask-based web application designed to help users assess suspicious messages. It checks text against configurable warning patterns and produces a risk score with a risk category.

The project also explores how Ring event integrations could support a broader digital safety experience. **Live Ring API or simulator integration is not yet implemented in this version.**

## Current Features

- Web dashboard for entering suspicious text.
- Flask backend for processing analysis requests.
- Rule-based warning pattern detection.
- Risk score from 0 to 100.
- Low, medium, and high risk categories.
- Safety reminder explaining that a low score does not guarantee safety.

## Technology Stack

- Python
- Flask
- HTML
- CSS
- JavaScript

## Requirements

- Python 3.10 or later
- pip

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment:

   `python -m venv .venv`

4. Activate it on Windows:

   `.venv\Scripts\Activate.ps1`

5. Install dependencies:

   `pip install -r requirements.txt`

6. Start the application:

   `python app.py`

7. Open `http://127.0.0.1:5000/` in your browser.

## Limitations

The current analyzer uses configured warning patterns. It is not a trained machine-learning model, and its scores are indicators rather than proof that a message is safe or malicious. Ring integration requires additional implementation and testing.

## License

This project is released under the MIT License. See the LICENSE file.

