document.addEventListener("DOMContentLoaded", () => {
  // Get textArea element by ID
  const textarea = document.getElementById("email-text");
  const form = document.getElementById("phishing-form");

  const API_URL = "http://localhost:8000";
  const resultContainer = document.querySelector(".result-container");
  const resultText = document.getElementById("result-text");

  // Get the CSRF token from the hidden input field that Django creates
  const csrfToken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]',
  ).value;

  // FetchAPI
  form.addEventListener("submit", async (event) => {
    // 1. prevent default form submission  (which reloads the page)
    event.preventDefault();

    // Get email text from the textArea
    const emailText = textarea.value.trim();

    // Do not send any empty request
    if (!emailText) return;

    // Prepare the  data to be sent to the server
    const formData = {
      email_text: emailText,
    };

    // 2. Use the fetchAPI  to send the form data to backend
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

      // Update the content of result container with the prediction
      resultText.textContent = result;
      // 5. Update the hidden container
      resultContainer.style.display = "block";
      // 6. Display the container by changing its cs
    } catch (error) {
      // Handle any errors that occur during the fetch operation
      console.error("There was a problem with the fetch operation:", error);
      resultText.textContent = "Error: Could not get a result from the server.";
      resultContainer.style.display = "block";
    }
  });
});
