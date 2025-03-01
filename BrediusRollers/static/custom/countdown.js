const date = document.getElementById('date').textContent.trim();
const [D, M, Y] = date.split(' ');

// Map non-English months to English
const monthMap = {
  'jan': 'jan', 'januari': 'jan', 'feb': 'feb', 'februari': 'feb', 'mrt': 'mar', 'maart': 'mar',
  'apr': 'apr', 'april': 'apr', 'mei': 'may', 'jun': 'jun', 'juni': 'jun',
  'jul': 'jul', 'juli': 'jul', 'aug': 'aug', 'augustus': 'aug', 'sep': 'sep', 'september': 'sep',
  'okt': 'oct', 'oktober': 'oct', 'nov': 'nov', 'november': 'nov', 'dec': 'dec', 'december': 'dec'
};

// Convert month to English (if needed)
const engMonth = monthMap[M] || M;

const ndate = `${engMonth} ${D}, ${Y}`;
const countDownDate = new Date(ndate).getTime();

console.log(ndate);  // Check formatted date
console.log(countDownDate); // Ensure valid timestamp

var x = setInterval(function() {

    // Get today's date and time
    var now = new Date().getTime();
  
    // Find the distance between now and the count down date
    var distance = countDownDate - now;
  
    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  
    // Display the result in the element with id="demo"
    document.getElementById("countdown-box").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
  
    // If the count down is finished, write some text
    if (distance < 0) {
      clearInterval(x);
      document.getElementById("countdown-box").innerHTML = "BEZIG";
    }
  }, 1000);

  