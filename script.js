// API Base URL - Change this when deploying the backend to production!
const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("tts-form");
    const resultContainer = document.getElementById("result-container");
    const loadingDiv = document.getElementById("loading");
    const audioOutputDiv = document.getElementById("audio-output");
    const errorMessageDiv = document.getElementById("error-message");
    
    const audioPlayer = document.getElementById("audio-player");
    const downloadBtn = document.getElementById("download-btn");
    const errorText = document.getElementById("error-text");

    function showError(message) {
        loadingDiv.classList.add("hidden");
        audioOutputDiv.classList.add("hidden");
        errorMessageDiv.classList.remove("hidden");
        errorText.textContent = message;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // UI State: Loading
        resultContainer.classList.remove("hidden");
        loadingDiv.classList.remove("hidden");
        audioOutputDiv.classList.add("hidden");
        errorMessageDiv.classList.add("hidden");

        const apiKey = document.getElementById("api-key").value.trim();
        const text = document.getElementById("text-input").value.trim();
        const language = document.getElementById("language-select").value;
        const gender = document.getElementById("gender-select").value;

        if (!apiKey) {
            showError("API Key is required!");
            return;
        }

        try {
            // STEP 1: Generate Audio (Get Job ID)
            const generateFormData = new FormData();
            generateFormData.append("text", text);
            generateFormData.append("language", language);
            generateFormData.append("gender", gender);

            const generateResponse = await fetch(`${API_BASE_URL}/generate`, {
                method: "POST",
                headers: {
                    "X-API-Key": apiKey
                },
                body: generateFormData
            });

            if (!generateResponse.ok) {
                const errData = await generateResponse.json().catch(() => ({}));
                console.error("Generate Error:", errData);
                throw new Error(errData.detail || `Failed to generate audio (Status ${generateResponse.status})`);
            }

            const { job_id } = await generateResponse.json();
            console.log("Audio generated successfully. Job ID:", job_id);

            // STEP 2: Download Audio using Job ID
            const downloadFormData = new FormData();
            downloadFormData.append("job_id", job_id);

            const downloadResponse = await fetch(`${API_BASE_URL}/download`, {
                method: "POST",
                headers: {
                    "X-API-Key": apiKey
                },
                body: downloadFormData
            });

            if (!downloadResponse.ok) {
                const errData = await downloadResponse.json().catch(() => ({}));
                console.error("Download Error:", errData);
                throw new Error(errData.detail || "Failed to download generated audio.");
            }

            // Create Audio Blob URL
            const audioBlob = await downloadResponse.blob();
            console.log("Audio downloaded. Blob size:", audioBlob.size);
            const audioUrl = URL.createObjectURL(audioBlob);

            // Update UI
            audioPlayer.src = audioUrl;
            audioPlayer.load(); // Ensure the browser loads the new blob URL
            downloadBtn.href = audioUrl;
            downloadBtn.download = job_id + ".wav"; // Give the file a proper name
            
            loadingDiv.classList.add("hidden");
            audioOutputDiv.classList.remove("hidden");
            
            console.log("UI updated. Audio output should be visible.");

            // Optional: Auto-play the audio
            audioPlayer.play().catch(e => console.log("Autoplay blocked:", e));

        } catch (error) {
            console.error("TTS Error:", error);
            showError(error.message || "An unexpected error occurred.");
        }
    });
});
