from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from models.predict import classify_tumor, segment_tumor
from model import db, AnalysisResult  # Import database

app = Flask(__name__)

# Upload and result folders
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tumor_user:10152021@localhost/brain_tumor_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')

        if 'mri_image' not in request.files:
            return render_template('index.html', tumor=None)

        file = request.files['mri_image']
        if file.filename == '':
            return render_template('index.html', tumor=None)

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        print(f"✅ Saved original image at: {save_path}")
        print(f"✅ File exists after save? {os.path.exists(save_path)}")

        # Run classification
        tumor_type = classify_tumor(save_path)
        print(f"✅ Classification result: {tumor_type}")

        # Convert path to web-safe format
        original_image_url = f"/static/uploads/{filename}"

        if tumor_type.lower() == 'no tumor':
            print("🛑 No tumor detected. Skipping segmentation.")
            # Save to database
            new_result = AnalysisResult(
                patient_name=name,
                image_path=original_image_url,
                prediction_label=tumor_type,
                prediction_mask_path=None
            )
            db.session.add(new_result)
            db.session.commit()

            return render_template('index.html',
                                   tumor=tumor_type,
                                   original_image=original_image_url,
                                   image_path=None,
                                   outlined_image=None)
        else:
            # Run segmentation only if tumor is present
            segmented_paths = segment_tumor(save_path, app.config['RESULT_FOLDER'])
            segmented_path = segmented_paths['overlay_path']
            outlined_path = segmented_paths['outlined_path']

        print(f"✅ Saved segmented image at: {segmented_path}")
        print(f"✅ Segmentation file exists? {os.path.exists(segmented_path)}")

        # Convert paths to web-safe format
        segmented_image_url = f"/static/results/segmented_{filename}".replace("\\", "/")
        outlined_image_url = f"/static/results/outlined_{filename}".replace("\\", "/")

        # Save to database
        new_result = AnalysisResult(
            patient_name=name,
            image_path=original_image_url,
            prediction_label=tumor_type,
            prediction_mask_path=outlined_image_url
        )
        db.session.add(new_result)
        db.session.commit()

        return render_template('index.html',
                               tumor=tumor_type,
                               original_image=original_image_url,
                               image_path=segmented_image_url,
                               outlined_image=outlined_image_url)

    return render_template('index.html')

# Optional: History route
@app.route('/history')
def history():
    results = AnalysisResult.query.order_by(AnalysisResult.timestamp.desc()).all()
    return render_template('history.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)