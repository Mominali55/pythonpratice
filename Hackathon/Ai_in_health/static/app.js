document.addEventListener("DOMContentLoaded", () => {
    
    // UI Elements
    const patientForm = document.getElementById("patientForm");
    const clearBtn = document.getElementById("clearBtn");
    const analyzeBtn = document.getElementById("analyzeBtn");
    
    // Results Dashboard Elements
    const emptyState = document.getElementById("emptyState");
    const predictionBanner = document.getElementById("predictionBanner");
    const alertTitle = document.getElementById("alertTitle");
    const alertMessage = document.getElementById("alertMessage");

    // Handle Form Submit
    patientForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // 1. Gather & Format Data
        const formData = new FormData(patientForm);
        const dataPayload = {
            age: parseFloat(formData.get("age")),
            sex: parseInt(formData.get("sex")),
            cp: parseInt(formData.get("cp")),
            trestbps: parseFloat(formData.get("trestbps")),
            chol: parseFloat(formData.get("chol")),
            fbs: parseInt(formData.get("fbs")),
            restecg: parseInt(formData.get("restecg")),
            thalach: parseFloat(formData.get("thalach")),
            exang: parseInt(formData.get("exang")),
            oldpeak: parseFloat(formData.get("oldpeak")),
            slope: parseInt(formData.get("slope")),
            ca: parseInt(formData.get("ca")),
            thal: parseInt(formData.get("thal"))
        };

        // Extra client-side validation logic (already partly handled by HTML5 min/max)
        if (dataPayload.age < 20 || dataPayload.age > 120) {
            alert("Age must be between 20 and 120.");
            return;
        }
        
        // Disable button while processing
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";

        try {
            // 2. Send POST Request to /predict
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(dataPayload)
            });

            if (!response.ok) {
                throw new Error("API request failed with status: " + response.status);
            }

            const result = await response.json();
            
            // 3. Update Dashboard Logic
            displayResult(result.prediction);

        } catch (error) {
            console.error("Error during analysis:", error);
            alert("An error occurred while connecting to the AI system.");
        } finally {
            // Reset button
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = "Analyze Results";
        }
    });

    // Display appropriate results banner
    function displayResult(prediction) {
        // Hide empty state
        emptyState.classList.add("hidden");
        
        // Remove existing classes
        predictionBanner.className = "alert";
        
        if (prediction === 0) {
            // Healthy / Low Risk
            predictionBanner.classList.add("alert-healthy");
            alertTitle.textContent = "Healthy / Low Risk";
            alertMessage.textContent = "Based on the provided diagnostic metrics, the model predicts a low probability of cardiovascular disease.";
        } else if (prediction === 1) {
            // High Risk
            predictionBanner.classList.add("alert-risk");
            alertTitle.textContent = "High Risk of Cardiovascular Disease";
            alertMessage.textContent = "The clinical decision support system has flagged this patient as high-risk. Further cardiological evaluation is strongly recommended.";
        }
        
        // Show banner
        predictionBanner.classList.remove("hidden");
    }

    // Handle Clear Form
    clearBtn.addEventListener("click", () => {
        patientForm.reset();
        
        // Reset Dashboard
        emptyState.classList.remove("hidden");
        predictionBanner.classList.add("hidden");
        predictionBanner.className = "alert hidden"; // reset specific alert classes
    });
});
