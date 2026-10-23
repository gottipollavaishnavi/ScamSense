
from flask import Flask, request, jsonify

app = Flask(__name__)


def analyze_risk(description):
    text = description.lower()
    findings = []

    checks = [
        (["otp", "verification code"], "Requests an OTP or verification code", 35),
        (["password", "bank credentials"], "Requests sensitive credentials", 35),
        (["urgent payment", "transfer money", "pay now"],
         "Pressures the user to make a payment", 30),
        (["account will be blocked", "act immediately", "last warning"],
         "Uses urgency or a threat", 20),
        (["click this link", "scan this qr"],
         "Asks you to follow an unverified link or QR code", 15),
    ]

    for phrases, reason, points in checks:
        if any(phrase in text for phrase in phrases):
            findings.append({"reason": reason, "points": points})

    score = min(100, sum(item["points"] for item in findings))

    if score >= 60:
        level = "HIGH"
        advice = "Do not share codes or pay. Verify the claim through an official channel."
    elif score >= 30:
        level = "MEDIUM"
        advice = "Pause and independently verify the person's identity."
    else:
        level = "LOW"
        advice = "No configured warning patterns matched. This does not prove safety."

    return {
        "risk_score": score,
        "risk_level": level,
        "findings": findings,
        "advice": advice
    }


@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ScamSense | Digital Safety Shield</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0; padding: 30px 18px;
    background: #0b1020; color: #edf3ff;
    font-family: Arial, sans-serif;
}
main { max-width: 850px; margin: 25px auto; }
header, section {
    background: #121a2d; border: 1px solid #26334c;
    border-radius: 16px; padding: 25px; margin-bottom: 20px;
}
header { border-top: 3px solid #72e3c0; }
h1 { color: #72e3c0; font-size: 38px; margin-bottom: 8px; }
h2 { font-size: 21px; }
p { line-height: 1.65; }
.muted { color: #98a8c3; }
textarea {
    display: block; width: 100%; min-height: 130px;
    padding: 14px; margin: 12px 0;
    background: #0b1222; color: white;
    border: 1px solid #52617a; border-radius: 9px;
    font: inherit;
}
button {
    padding: 13px 18px; border: 0; border-radius: 8px;
    background: #72e3c0; color: #071a18;
    font-weight: bold; cursor: pointer;
}
button:disabled { opacity: .6; }
#result {
    margin-top: 20px; padding: 18px;
    border: 1px solid #52617a; border-radius: 10px;
}
.hidden { display: none; }
footer { color: #98a8c3; font-size: 12px; line-height: 1.6; }
</style>
</head>
<body>
<main>
<header>
    <p class="muted">YOUR PERSONAL DIGITAL SAFETY SHIELD</p>
    <h1>ScamSense 🛡️</h1>
    <p>Spot suspicious requests. Understand the warning signs. Make safer decisions.</p>
</header>

<section>
    <h2>Analyze a suspicious interaction</h2>
    <p class="muted">Describe a suspicious message, phone call, or visitor interaction.
    Never enter real passwords, OTPs, or financial details.</p>

    <form id="form">
        <label for="description">What happened?</label>
        <textarea id="description" required maxlength="1000"
        placeholder="Example: A caller says my bank account will be blocked unless I share my OTP and make an urgent payment."></textarea>
        <button id="analyzeButton" type="submit">Analyze Safety Risk →</button>
    </form>
    <div id="result" class="hidden" aria-live="polite"></div>
</section>

<section>
    <h2>How ScamSense helps</h2>
    <p>🔎 <strong>Warning signs:</strong> Identify configured suspicious phrases.</p>
    <p>🛡️ <strong>Risk explanation:</strong> Understand why a request may be dangerous.</p>
    <p>✅ <strong>Safer next steps:</strong> Verify claims using an independently obtained official contact.</p>
    <p class="muted">Ring integration is not connected yet. This is the initial working prototype.</p>
</section>

<footer>
ScamSense is a rule-based prototype, not proof of fraud. A low score does not guarantee
safety. Verify suspicious requests independently.
</footer>
</main>

<script>
const form = document.getElementById("form");
const result = document.getElementById("result");
const button = document.getElementById("analyzeButton");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    button.disabled = true;
    result.classList.remove("hidden");
    result.textContent = "Analyzing...";

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                description: document.getElementById("description").value
            })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Analysis failed");

        result.replaceChildren();

        const heading = document.createElement("h2");
        heading.textContent = data.risk_level + " RISK — " + data.risk_score + "/100";
        result.appendChild(heading);

        const advice = document.createElement("p");
        advice.textContent = data.advice;
        result.appendChild(advice);

        const title = document.createElement("strong");
        title.textContent = "Warning signs detected:";
        result.appendChild(title);

        const list = document.createElement("ul");
        data.findings.forEach(function(item) {
            const li = document.createElement("li");
            li.textContent = item.reason;
            list.appendChild(li);
        });
        result.appendChild(list);

        if (data.findings.length === 0) {
            const note = document.createElement("p");
            note.textContent = "No configured warning patterns matched. This does not prove safety.";
            result.appendChild(note);
        }
    } catch (error) {
        result.textContent = "Error: " + error.message;
    } finally {
        button.disabled = false;
    }
});
</script>
</body>
</html>
"""


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    description = str(data.get("description", "")).strip()

    if not description:
        return jsonify({"error": "Enter a description to analyze."}), 400

    return jsonify(analyze_risk(description))


if __name__ == "__main__":
    print("Starting ScamSense...", flush=True)
    app.run(host="127.0.0.1", port=5000, debug=False)
