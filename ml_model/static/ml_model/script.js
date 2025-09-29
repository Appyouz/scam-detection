document.addEventListener("DOMContentLoaded", () => {
  // Get textArea element by ID
  const textarea = document.getElementById("email-text");
  const form = document.getElementById("phishing-form");

  const resultContainer = document.querySelector(".result-container");
  const resultText = document.getElementById("result-text");

  // Get the CSRF token from the hidden input field that Django creates
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]',
  ).value;

  // FetchAPI
  form.addEventListener("submit", async (event) => {
    // 1. prevent default form submission (which reloads the page)
    event.preventDefault();

    // Get email text from the textArea
    const emailText = textarea.value.trim();

    // Do not send any empty request
    if (!emailText) return;

    // --- Added loading state and cleared old classes here ---
    // Clear previous classes and show loading state
    resultText.textContent = "Analyzing...";
    resultText.classList.remove("safe", "malicious");
    resultContainer.style.display = "block";

    // Prepare the  data to be sent to the server
    const formData = {
      email_text: emailText,
    };

    // 2. Use the fetchAPI to send the form data to backend
    try {
      const response = await fetch("/prediction_api/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },

        body: JSON.stringify(formData),
      });

      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);

      // 3.  Wait for server response
      const data = await response.json();
      // 4. Parse the received
      const result = data.result;

      // Apply the correct color class based on the prediction ---
      if (result === "Safe") {
        resultText.classList.add("safe");
      } else if (result === "Malicious") {
        resultText.classList.add("malicious");
      }
      // -----------------------------------------------------------------------

      // Update the content of result container with the prediction
      resultText.textContent = result;
      // 5. The container is already visible from the pre-fetch step.
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
      resultText.textContent = "Error: Could not get a result from the server.";
      // Ensure color classes are removed on error
      resultText.classList.remove("safe", "malicious");
      resultContainer.style.display = "block";
    }
  });
});
