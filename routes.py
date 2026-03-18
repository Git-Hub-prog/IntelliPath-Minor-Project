from flask import render_template, request, jsonify

def register_routes(app):
    @app.route('/')
    def index():
        """Serve the main landing page."""
        return render_template('index.html')

    @app.route('/assessment')
    def assessment():
        """Serve the assessment page."""
        return render_template('assessment.html')

    @app.route('/careers')
    def careers_page():
        """Serve the all careers page."""
        return render_template('careers.html')

    @app.route('/result')
    def result_page():
        """Serve the assessment result page."""
        return render_template('result.html')

    @app.route('/assessment/submit', methods=['POST'])
    def submit_assessment():
        """
        Handle assessment submission.
        Expects JSON: { "q1": "value", "q2": "value", ... }
        """
        try:
            answers = request.get_json()
            if not answers:
                return jsonify({"error": "No answers provided"}), 400

            # Process scores using the logic defined in app.py or a dedicated module
            # For modularity, we use a function injected or available via app context
            results = app.calculate_scores(answers)
            
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
