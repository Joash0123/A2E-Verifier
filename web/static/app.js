function parseJson(id) {
    return JSON.parse(document.getElementById(id).value);
}

async function verifyAction() {
    const resultPanel = document.getElementById("result");

    try {
        const authorized = {
            tool: document.getElementById("authorized-tool").value,
            operation: document.getElementById("authorized-operation").value,
            resource: document.getElementById("authorized-resource").value,
            parameters: parseJson("authorized-parameters"),
            context: parseJson("authorized-context"),
            actor: document.getElementById("authorized-actor").value
        };

        const executed = {
            tool: document.getElementById("executed-tool").value,
            operation: document.getElementById("executed-operation").value,
            resource: document.getElementById("executed-resource").value,
            parameters: parseJson("executed-parameters"),
            context: parseJson("executed-context"),
            actor: document.getElementById("executed-actor").value
        };

        const response = await fetch("/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                authorized,
                executed
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Verification request failed.");
        }

        resultPanel.classList.remove("hidden");

        document.getElementById("verdict").textContent =
            data.allowed ? "ALLOWED — MATCH" : "BLOCKED — " + data.verdict;

        document.getElementById("category").textContent =
            data.investigation.category;

        const evidence = document.getElementById("evidence");
        evidence.innerHTML = "";

        data.investigation.evidence.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            evidence.appendChild(li);
        });

        const remediation = document.getElementById("remediation");
        remediation.innerHTML = "";

        data.investigation.remediation.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            remediation.appendChild(li);
        });

        const aiPanel = document.getElementById("ai-investigation");

        if (aiPanel) {
            if (data.ai_investigation) {
                aiPanel.textContent = data.ai_investigation;
                aiPanel.classList.remove("hidden");
            } else {
                aiPanel.textContent =
                    "AI investigation unavailable. Set GROQ_API_KEY to enable AI analysis.";
                aiPanel.classList.remove("hidden");
            }
        }

        document.getElementById("details").textContent =
            JSON.stringify(data, null, 2);

    } catch (error) {
        resultPanel.classList.remove("hidden");

        document.getElementById("verdict").textContent =
            "ERROR — " + error.message;

        document.getElementById("category").textContent = "INVALID_INPUT";

        document.getElementById("evidence").innerHTML =
            "<li>Check that Parameters and Context contain valid JSON.</li>";

        document.getElementById("remediation").innerHTML =
            "<li>Correct the input and try again.</li>";

        const aiPanel = document.getElementById("ai-investigation");
        if (aiPanel) {
            aiPanel.textContent = "";
            aiPanel.classList.add("hidden");
        }

        document.getElementById("details").textContent = "";
    }
}

document
    .getElementById("verify-button")
    .addEventListener("click", verifyAction);
