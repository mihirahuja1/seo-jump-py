import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from user_management import check_user_credits
from domain_analysis import analyze_domain, insert_result_into_db
from supabase import create_client

load_dotenv()  # Load environment variables from .env.local

app = Flask(__name__)
CORS(app)

url = os.getenv("SUPABASE_URL", "url")
key = os.getenv("SUPABASE_KEY", "key")
supabase = create_client(url, key)


@app.route("/analyze-domain", methods=["POST"])
def get_domain_analysis():
    logging.info("Request received for domain analysis")
    data = request.get_json()
    logging.debug(
        f"Received data: {data}"
    )  # Additional logging to debug the data received

    print(data)
    domain = data["domain"]
    user_id = data["userId"]

    credits_check, credits = check_user_credits(user_id, supabase)
    if not credits_check:
        logging.error("User credit check failed")
        return jsonify({"error": "Insufficient credits or invalid user"}), 403

    logging.debug("Credits check passed")
    try:
        result = analyze_domain(domain)
        logging.info(f"Analysis result: {result}")
        insert_result_into_db(result, user_id, domain, credits, supabase)
        print(result)
        return jsonify({"result":result})
    except Exception as e:
        logging.error(f"Error during domain analysis: {str(e)}")
        return jsonify({"error": "Error processing your request"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
