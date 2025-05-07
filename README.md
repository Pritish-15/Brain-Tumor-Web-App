# Brain Tumor Classification & Segmentation Web Application

## Project Description
This project is a Flask-based web application designed for the classification and segmentation of brain tumors from MRI images. Users can upload MRI scans, and the application will classify the type of tumor present (if any) and provide a segmented overlay and tumor outline for visualization. The results are stored in a PostgreSQL database for future reference and analysis.

## Features
- Upload MRI images with patient information (name, age, gender).
- Automatic brain tumor classification.
- Tumor segmentation with overlay and outline visualization.
- Stores analysis results in a PostgreSQL database.
- View history of past analyses with patient details and prediction results.
- User-friendly web interface built with Bootstrap.

## Installation

### Prerequisites
- Python 3.7 or higher
- PostgreSQL database server
- pip package manager

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd brain-tumor-webapp
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: If `requirements.txt` is not present, install Flask, Flask-SQLAlchemy, psycopg2, and other dependencies manually.)*

4. Set up PostgreSQL database:
   - Create a database named `brain_tumor_app`.
   - Create a user `tumor_user` with password `10152021`.
   - Grant necessary privileges to the user on the database.

5. Configure database URI in `app.py` if needed:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tumor_user:10152021@localhost/brain_tumor_app'
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000/
   ```

3. Fill in patient details and upload an MRI image.

4. Submit the form to receive tumor classification and segmentation results.

5. View past analysis results by navigating to:
   ```
   http://localhost:5000/history
   ```

## Folder Structure

```
brain-tumor-webapp/
│
├── app.py                  # Main Flask application
├── model.py                # Database model definitions
├── test.py                 # PostgreSQL connection test script
├── models/                 # Contains model-related scripts (e.g., classification, segmentation)
├── static/                 # Static files (uploads, results)
│   ├── uploads/            # Uploaded MRI images
│   └── results/            # Segmentation result images
├── templates/              # HTML templates for the web interface
│   ├── index.html          # Main upload and result page
│   └── history.html        # Past analysis history page
└── utils/                  # Utility scripts (if any)
```

## Notes
- The classification and segmentation logic is implemented in the `models/predict.py` file.
- Ensure the PostgreSQL server is running before starting the application.
- Uploaded images and results are stored in the `static/uploads` and `static/results` directories respectively.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.
