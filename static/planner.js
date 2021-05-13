

//stopwatch
var timeElapsed = 0,
    swIntervalID = 0;

function startStopwatch() {
    if (swIntervalID == 0)
        swIntervalID = setInterval(function() {
            timeElapsed++;
            var sec = timeElapsed % 60,
                min = Math.trunc(timeElapsed / 60) % 60,
                hour = Math.trunc(timeElapsed / 3600);

            if (sec < 10)
                sec = "0" + sec;

            if (min < 10)
                min = "0" + min;

            if (hour < 10)
                hour = "0" + hour;

            document.getElementById("stopwatch").innerHTML = hour + " : " + min + " : " + sec;
        }, 1000);
}

function stopStopwatch() {
    clearInterval(swIntervalID);
    swIntervalID = 0;
}

function resetStopwatch() {
    stopStopwatch();
    timeElapsed = 0;
    document.getElementById("stopwatch").innerHTML = "00 : 00 : 00";
}




//clock
var week_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    month_word = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function clock(){
    var d = new Date();
    var wday = d.getDay(), month = d.getMonth(), day = d.getDate(), year = d.getFullYear(),
        hour = d.getHours(), min = d.getMinutes(), sec = d.getSeconds();

    if (day < 10)
        day = "0" + day;

    if (min < 10)
        min = "0" + min;

    if (sec < 10)
        sec = "0" + sec;

    var ids = ["dayofweek", "date", "time"];
    var printclock = [week_days[wday], month_word[month] + " " + day + ", " + year, hour + " : " + min + " : " + sec];

    for (var i = 0; i < ids.length; i++)
        document.getElementById(ids[i]).innerHTML = printclock[i];

    setInterval(clock, 1000);
}

window.onload=clock;




//timer
var totalTime = 0,
    timerSet = 0,
    display = "00 : 00 : 00",
    stopped = false,
    timerIntervalID = 0;

function setTimer() {
    var nhour = parseInt(document.getElementById("hour").value, 10),
        nmin = parseInt(document.getElementById("min").value, 10),
        nsec = parseInt(document.getElementById("sec").value, 10);

    if (isNaN(nhour)) nhour = 0;
    if (isNaN(nmin)) nmin = 0;
    if (isNaN(nsec)) nsec = 0;

    timerSet = nhour * 3600 + nmin * 60 + nsec;
    totalTime = timerSet;

    var sec = nsec % 60,
        min = (Math.trunc(nsec / 60) + nmin) % 60,
        hour = Math.trunc((Math.trunc(nsec / 60) + nmin) / 60) + nhour;

    if (sec < 10)
        sec = "0" + sec;

    if (min < 10)
        min = "0" + min;

    if (hour < 10)
        hour = "0" + hour;

    display = hour + " : " + min + " : " + sec;
    document.getElementById("timer").innerHTML = display;
}

function startTimer() {
    if (timerIntervalID == 0 && totalTime > 0)
        timerIntervalID = setInterval(function() {
            totalTime--;
            var sec = totalTime % 60,
                min = Math.trunc(totalTime / 60) % 60,
                hour = Math.trunc(totalTime / 3600);

            if (sec < 10)
                sec = "0" + sec;

            if (min < 10)
                min = "0" + min;

            if (hour < 10)
                hour = "0" + hour;

            document.getElementById("timer").innerHTML = hour + " : " + min + " : " + sec;

            if (totalTime <= 0) {
                stopped = false;
                timerEnd();
            }
        }, 1000);
}

function stopTimer() {
    clearInterval(timerIntervalID);
    if (totalTime > 0) timerIntervalID = 0;
    stopped = true;
}

function resetTimer() {
    totalTime = timerSet;
    stopTimer();
    document.getElementById("timer").innerHTML = display;
}

async function timerEnd() {
    clearInterval(timerIntervalID);
    var count = 0;

    while (!stopped) {
        document.getElementById("timer").style.color = "#ff5555";
        await new Promise(resolve => setTimeout(resolve, 500));
        document.getElementById("timer").style.color = "black";
        await new Promise(resolve => setTimeout(resolve, 500));

        count++;
        if (count > 300) { stopTimer(); }
    }
}