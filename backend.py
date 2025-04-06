from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the abuse classifier
classifier = pipeline("text-classification", model="akp26/abusemodel")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        regions = data.get("regions", [])
        all_regions = []
        toxic_regions = []

        for region in regions:
            text = region.get("text", "")
            if not text.strip():
                continue

            result = classifier(text, truncation=True)[0]

            
            region["label"] = result["label"]
            region["score"] = result["score"]
            all_regions.append(region)

            
            if result["label"] == "LABEL_0":
                toxic_regions.append(region)

            print(f"→ Label: {result['label']} | Score: {result['score']:.4f} | Text: {text}")

        return jsonify({
            "all_regions": all_regions,
            "toxic_regions": toxic_regions
        })

    except Exception as e:
        print(f"[x] Error in /predict: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)