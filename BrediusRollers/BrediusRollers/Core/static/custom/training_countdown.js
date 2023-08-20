console.log("Idiot")

const training = document.getElementById('training-countdown');
const [a, b, c, d, e, f] = training.textContent.split(' ');

const [training_countdown] = [d + " " + e + ", " + f + " " + b]

var TrainingCountDownDate = new Date(training_countdown).getTime();

console.log(training_countdown)




var x = setInterval(function() {

    // Get today's date and time
    var now = new Date().getTime();
  
    // Find the distance between now and the count down date
    var distance = TrainingCountDownDate - now;
  
    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  
    // Display the result in the element with id="demo"
    document.getElementById("training-countdown-box").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
  
    // If the count down is finished, write some text
    if (distance < 0) {
      clearInterval(x);
      document.getElementById("training-countdown-box").innerHTML = "BEZIG";
    }
  }, 1000);

  



