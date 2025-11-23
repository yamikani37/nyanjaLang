from flask import Flask, render_template, request, jsonify
from io import StringIO
from nyanja.runtime import execute_nyanja_code 

app = Flask(__name__)

@app.route("/")
def index():
    """Renders the main page with the code editor."""
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    """
    Receives NyanjaLang code via POST request, executes it,
    and returns the output/errors as JSON.
    """
    code = request.form.get("code", "") 
    
    # Create StringIO objects to capture stdout and stderr separately
    output_buffer = StringIO()
    error_buffer = StringIO()
    _ = execute_nyanja_code(
        code, 
        output_stream=output_buffer, 
        error_stream=error_buffer
    )
    

    captured_output = output_buffer.getvalue().strip()
    captured_errors = error_buffer.getvalue().strip()
    response = {
        "output": captured_output,
        "errors": captured_errors
    }

   
    if captured_errors:
        return jsonify(response), 400
    else:
        return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=False)  # Set debug=False for production