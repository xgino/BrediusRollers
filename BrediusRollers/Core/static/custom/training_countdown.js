document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("training-countdown");
    const box = document.getElementById("training-countdown-box");

    if (!el || !box) return;

    // Extract text from div (example: "maandag 06:00 | 03 maart 2025")
    const [timePart, datePart] = el.textContent.trim().split(" | ");
    const time = timePart.split(" ")[1]; // Extracts "06:00"
    const [day, monthDutch, year] = datePart.split(" "); // Extracts [03, maart, 2025]

    // Map Dutch months to English
    const monthMap = {
        "januari": "January", "februari": "February", "maart": "March", "april": "April",
        "mei": "May", "juni": "June", "juli": "July", "augustus": "August",
        "september": "September", "oktober": "October", "november": "November", "december": "December"
    };

    const month = monthMap[monthDutch.toLowerCase()];
    if (!month) return console.error("Invalid month:", monthDutch);

    // Create a valid Date object
    const targetDate = new Date(`${month} ${day}, ${year} ${time}`).getTime();
    if (isNaN(targetDate)) return console.error("Invalid date format:", targetDate);

    // Countdown function
    const updateCountdown = () => {
        const now = Date.now();
        const diff = targetDate - now;

        if (diff <= 0) {
            box.textContent = "BEZIG";
            clearInterval(interval);
            return;
        }

        const d = Math.floor(diff / (1000 * 60 * 60 * 24));
        const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((diff % (1000 * 60)) / 1000);

        box.textContent = `${d}d ${h}h ${m}m ${s}s`;
    };

    // Start countdown
    const interval = setInterval(updateCountdown, 1000);
    updateCountdown();
});
