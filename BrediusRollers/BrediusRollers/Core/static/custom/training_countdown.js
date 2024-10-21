document.addEventListener("DOMContentLoaded", function() {
  console.log("Idiot");

  // Get the countdown element
  const trainingCountdownElement = document.getElementById('training-countdown');

  // Check if the element exists
  if (!trainingCountdownElement) {
      console.error("Element with id 'training-countdown' not found.");
      return; // Exit if the element is not found
  }

  // Get the content from the training countdown element
  const trainingCountdownText = trainingCountdownElement.textContent; // e.g., "zaterdag 10:30 | 26 Okt 2024"
  console.log("Training Countdown Text:", trainingCountdownText); // Debugging line

  // Split the text to extract parts
  const parts = trainingCountdownText.split(' | ');

  // Ensure we have at least two parts to avoid undefined errors
  if (parts.length < 2) {
      console.error("Unexpected format in training countdown text.");
      return; // Exit if the format is unexpected
  }

  // Extract time and date
  const timePart = parts[0].trim(); // "zaterdag 10:30"
  const datePart = parts[1].trim(); // "26 Okt 2024"

  // Combine the extracted parts into a valid date string for JavaScript
  const formattedDateString = `${datePart} ${timePart.split(' ')[1]}`; // "26 Okt 2024 10:30"

  // Create a new Date object from the formatted string
  const trainingCountDownDate = new Date(formattedDateString.replace('Okt', 'October')).getTime();

  console.log("Training Count Down Date:", trainingCountDownDate);

  var x = setInterval(function() {
      // Get the current date and time
      var now = new Date().getTime();

      // Find the distance between now and the countdown date
      var distance = trainingCountDownDate - now;

      // Time calculations for days, hours, minutes, and seconds
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      // Display the result in the element with id="training-countdown-box"
      document.getElementById("training-countdown-box").innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

      // If the countdown is finished, write some text
      if (distance < 0) {
          clearInterval(x);
          document.getElementById("training-countdown-box").innerHTML = "BEZIG";
      }
  }, 1000);
});