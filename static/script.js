/**
 * script.js - Frontend Logic & Async Communication
 * AI Email & Message Assistant
 * Course: Generative AI (Weeks 1-3)
 * Author: Generative AI Student
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements - Inputs
    const messageForm = document.getElementById("messageForm");
    const messageTypeSelect = document.getElementById("messageType");
    const messageToneSelect = document.getElementById("messageTone");
    const roughMessageArea = document.getElementById("roughMessage");
    const charCounter = document.getElementById("charCounter");
    const lengthPreferenceSelect = document.getElementById("lengthPreference");
    const urduToggle = document.getElementById("urduToggle");
    const presetChips = document.querySelectorAll(".preset-chip");

    // DOM Elements - Action Buttons
    const generateBtn = document.getElementById("generateBtn");
    const generateBtnText = document.getElementById("generateBtnText");
    const clearAllBtn = document.getElementById("clearAllBtn");
    const copyBtn = document.getElementById("copyBtn");
    const copyPillBtn = document.getElementById("copyPillBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const downloadPillBtn = document.getElementById("downloadPillBtn");
    const regenerateBtn = document.getElementById("regenerateBtn");
    const copySubjectBtn = document.getElementById("copySubjectBtn");

    // DOM Elements - State Containers
    const outputToolbar = document.getElementById("outputToolbar");
    const outputEmptyState = document.getElementById("outputEmptyState");
    const outputLoadingState = document.getElementById("outputLoadingState");
    const outputContentContainer = document.getElementById("outputContentContainer");
    
    // DOM Elements - Output Content
    const subjectBox = document.getElementById("subjectBox");
    const subjectText = document.getElementById("subjectText");
    const generatedText = document.getElementById("generatedText");
    const outputMetaTag = document.getElementById("outputMetaTag");
    const generationTimestamp = document.getElementById("generationTimestamp");

    // DOM Elements - Alerts & Notifications
    const errorAlert = document.getElementById("errorAlert");
    const errorMessage = document.getElementById("errorMessage");
    const toastNotification = document.getElementById("toastNotification");
    const toastMessage = document.getElementById("toastMessage");
    const apiStatusBadge = document.getElementById("apiStatusBadge");
    const apiStatusText = document.getElementById("apiStatusText");

    // State Variables
    let currentGeneratedFullMessage = "";
    let currentSubject = "";
    let currentMessageBody = "";
    let toastTimeout = null;

    /* -------------------------------------------------------------
       1. Character Counter & Text Area Input
       ------------------------------------------------------------- */
    roughMessageArea.addEventListener("input", () => {
        const charCount = roughMessageArea.value.length;
        const words = roughMessageArea.value.trim().split(/\s+/).filter(w => w.length > 0).length;
        charCounter.textContent = `${charCount} char${charCount === 1 ? '' : 's'} (${words} word${words === 1 ? '' : 's'})`;
        
        // Hide error when user starts typing
        if (charCount > 0 && !errorAlert.classList.contains("hidden")) {
            hideError();
        }
    });

    /* -------------------------------------------------------------
       2. Quick Preset Chips Handler
       ------------------------------------------------------------- */
    presetChips.forEach(chip => {
        chip.addEventListener("click", () => {
            const type = chip.getAttribute("data-type");
            const tone = chip.getAttribute("data-tone");
            const text = chip.getAttribute("data-text");

            if (type && messageTypeSelect) messageTypeSelect.value = type;
            if (tone && messageToneSelect) messageToneSelect.value = tone;
            if (text && roughMessageArea) {
                roughMessageArea.value = text;
                roughMessageArea.dispatchEvent(new Event("input"));
                roughMessageArea.focus();
            }
        });
    });

    /* -------------------------------------------------------------
       3. Error Alert Handling
       ------------------------------------------------------------- */
    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.classList.remove("hidden");
        // Scroll error into view on mobile if needed
        errorAlert.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    window.hideError = function() {
        errorAlert.classList.add("hidden");
    };

    /* -------------------------------------------------------------
       4. Toast Notifications
       ------------------------------------------------------------- */
    function showToast(message) {
        if (toastTimeout) {
            clearTimeout(toastTimeout);
        }
        toastMessage.textContent = message;
        toastNotification.classList.remove("hidden");

        toastTimeout = setTimeout(() => {
            toastNotification.classList.add("hidden");
        }, 3000);
    }

    /* -------------------------------------------------------------
       5. UI State Management (Empty, Loading, Result)
       ------------------------------------------------------------- */
    function setState(state) {
        // Hide all output states
        outputEmptyState.classList.add("hidden");
        outputLoadingState.classList.add("hidden");
        outputContentContainer.classList.add("hidden");

        if (state === "loading") {
            outputLoadingState.classList.remove("hidden");
            outputToolbar.classList.add("hidden");
            generateBtn.disabled = true;
            generateBtnText.textContent = "Generating...";
        } else if (state === "result") {
            outputContentContainer.classList.remove("hidden");
            outputToolbar.classList.remove("hidden");
            generateBtn.disabled = false;
            generateBtnText.textContent = "Generate with AI";
        } else {
            // "empty" state
            outputEmptyState.classList.remove("hidden");
            outputToolbar.classList.add("hidden");
            generateBtn.disabled = false;
            generateBtnText.textContent = "Generate with AI";
        }
    }

    /* -------------------------------------------------------------
       6. Generate Message via Fetch API
       ------------------------------------------------------------- */
    async function requestGeneration() {
        const rawMessage = roughMessageArea.value.trim();
        const messageType = messageTypeSelect.value;
        const tone = messageToneSelect.value;
        const lengthPref = lengthPreferenceSelect ? lengthPreferenceSelect.value : "balanced";
        const includeUrdu = urduToggle ? urduToggle.checked : false;

        // Frontend validation
        if (!rawMessage) {
            showError("Please enter your message. The input field cannot be empty.");
            roughMessageArea.focus();
            return;
        }

        hideError();
        setState("loading");

        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: rawMessage,
                    message_type: messageType,
                    tone: tone,
                    length: lengthPref,
                    include_urdu: includeUrdu
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                const err = data.error || "Unable to connect to the AI service. Please try again.";
                showError(err);
                setState(currentGeneratedFullMessage ? "result" : "empty");
                return;
            }

            // Successfully received response
            currentGeneratedFullMessage = data.generated_message;
            currentSubject = data.subject || "";
            currentMessageBody = data.body || data.generated_message;

            // Render Subject
            if (currentSubject) {
                subjectText.textContent = currentSubject;
                subjectBox.classList.remove("hidden");
            } else {
                subjectBox.classList.add("hidden");
            }

            // Render Body
            generatedText.textContent = currentMessageBody;

            // Update Metadata
            outputMetaTag.textContent = `${data.message_type} • ${data.tone} Tone`;
            const now = new Date();
            generationTimestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            setState("result");
            showToast("Message successfully generated!");

        } catch (error) {
            console.error("Fetch generation error:", error);
            showError("Unable to connect to the AI service. Please check your network and make sure the Flask server is running.");
            setState(currentGeneratedFullMessage ? "result" : "empty");
        }
    }

    /* -------------------------------------------------------------
       7. Copy to Clipboard Functionality
       ------------------------------------------------------------- */
    async function copyToClipboard(textToCopy, successMsg = "Copied to clipboard!") {
        if (!textToCopy) return;

        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(textToCopy);
            } else {
                // Fallback for non-https or older browsers
                const tempTextArea = document.createElement("textarea");
                tempTextArea.value = textToCopy;
                tempTextArea.style.position = "fixed";
                tempTextArea.style.left = "-9999px";
                document.body.appendChild(tempTextArea);
                tempTextArea.focus();
                tempTextArea.select();
                document.execCommand("copy");
                document.body.removeChild(tempTextArea);
            }
            showToast(successMsg);
        } catch (err) {
            console.error("Clipboard copy error:", err);
            showError("Failed to copy text. Please select and copy manually.");
        }
    }

    /* -------------------------------------------------------------
       8. Download as .txt File
       ------------------------------------------------------------- */
    function downloadMessageFile() {
        if (!currentGeneratedFullMessage) return;

        const category = messageTypeSelect.value.replace(/\s+/g, "_");
        const timestamp = new Date().toISOString().slice(0, 10);
        const filename = `AI_${category}_${timestamp}.txt`;

        const content = [
            `==================================================`,
            `  AI EMAIL & MESSAGE ASSISTANT - GENERATED OUTPUT `,
            `==================================================`,
            `Category: ${messageTypeSelect.value}`,
            `Writing Tone: ${messageToneSelect.value}`,
            `Generated On: ${new Date().toLocaleString()}`,
            `==================================================\n`,
            currentGeneratedFullMessage,
            `\n==================================================`,
            `Generated with Groq AI`
        ].join("\n");

        const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        showToast(`Saved as ${filename}`);
    }

    /* -------------------------------------------------------------
       9. Clear Inputs & Output
       ------------------------------------------------------------- */
    function clearAll() {
        roughMessageArea.value = "";
        charCounter.textContent = "0 characters";
        messageTypeSelect.selectedIndex = 0;
        messageToneSelect.selectedIndex = 0;
        if (lengthPreferenceSelect) lengthPreferenceSelect.value = "balanced";
        if (urduToggle) urduToggle.checked = false;

        currentGeneratedFullMessage = "";
        currentSubject = "";
        currentMessageBody = "";
        
        hideError();
        setState("empty");
        roughMessageArea.focus();
        showToast("Form cleared.");
    }

    /* -------------------------------------------------------------
       10. Event Listeners
       ------------------------------------------------------------- */
    generateBtn.addEventListener("click", requestGeneration);
    regenerateBtn.addEventListener("click", requestGeneration);
    clearAllBtn.addEventListener("click", clearAll);

    // Copy actions
    copyBtn.addEventListener("click", () => copyToClipboard(currentGeneratedFullMessage, "Full message copied to clipboard!"));
    copyPillBtn.addEventListener("click", () => copyToClipboard(currentGeneratedFullMessage, "Full message copied to clipboard!"));
    
    if (copySubjectBtn) {
        copySubjectBtn.addEventListener("click", () => copyToClipboard(currentSubject, "Subject line copied!"));
    }

    // Download actions
    downloadBtn.addEventListener("click", downloadMessageFile);
    downloadPillBtn.addEventListener("click", downloadMessageFile);

    // Ctrl+Enter or Cmd+Enter to generate quickly from textarea
    roughMessageArea.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            requestGeneration();
        }
    });

    /* -------------------------------------------------------------
       11. Check API Status on load
       ------------------------------------------------------------- */
    async function checkServerStatus() {
        try {
            const res = await fetch("/api/status");
            if (res.ok) {
                const data = await res.json();
                if (data.configured) {
                    apiStatusBadge.innerHTML = `
                        <span class="status-dot status-active"></span>
                        <span>Groq Active (${data.model})</span>
                    `;
                } else {
                    apiStatusBadge.innerHTML = `
                        <span class="status-dot status-warning"></span>
                        <span>Set API Key in .env</span>
                    `;
                }
            }
        } catch (e) {
            // Server offline or starting up
            console.warn("Status check failed:", e);
        }
    }

    checkServerStatus();
});

