from flask import Flask, request, render_template
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    match_percentage = None  # Initialize match_percentage variable

    if request.method == 'POST':
        # Check if the POST request has files
        if 'resume' in request.files and 'job_description' in request.files:
            resume = request.files['resume']
            job_description = request.files['job_description']

            # Save the uploaded files
            resume_path = "static/uploads/resume.docx"
            job_description_path = "static/uploads/job_description.docx"

            resume.save(resume_path)
            job_description.save(job_description_path)

            # Process the uploaded files
            resume_text = docx2txt.process(resume_path)
            job_description_text = docx2txt.process(job_description_path)

            text = [resume_text, job_description_text]

            # Perform cosine similarity
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text)
            similarity = cosine_similarity(count_matrix)

            # Calculate the match percentage
            match_percentage = similarity[0][1] * 100
            match_percentage = round(match_percentage, 2)

            resume_url = resume_path  # Set the resume URL

    return render_template('SmartRecruit.html', match_percentage=match_percentage)

if __name__ == '__main__':
    app.run(debug=True)
