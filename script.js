const startButton = document.getElementById('startButton');
var myVar = document.getElementById('domain').value;
document.getElementById('domain').addEventListener('change', function () {
    myVar = this.value;
    console.log(`Selected domain updated to: ${myVar}`);
});


document.getElementById('startButton').addEventListener('click', function () {
    document.getElementById('startButton').style.display = 'none';
    document.getElementById('stopButton').style.display = 'inline-block';
});
const stopButton = document.getElementById('stopButton');
document.getElementById('stopButton').addEventListener('click', function () {
    document.getElementById('stopButton').style.display = 'none';
    document.getElementById('startButton').style.display = 'inline-block';
});
let status = document.getElementById('status');
let ws;
let recognition;
let isRecognitionActive = false;
let recognitionTimeout;
let restart_status = false
let reposne_from_ws = ''



function startRecognition(selectedValue) {
    console.log(selectedValue, 'selectedValue')
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        console.log(recognition, 'recognition:')
        recognition.continuous = true;
        recognition.interimResults = false;

        recognition.onstart = () => {
            const timestamp = new Date().toLocaleString();
            console.log('started', timestamp);
            // status.innerText = 'Speech recognition is on. Speak into the microphone.';
            isRecognitionActive = true;
        };
        recognition.onresult = (event) => {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }


            // stop text-to-speech
            window.speechSynthesis.cancel();

            if (ws && ws.readyState === WebSocket.OPEN) {
                final_text = finalTranscript || interimTranscript;
                final_text = final_text + '#' + myVar;
                ws.send(final_text);
                console.log('sending', final_text);
            } else {
                console.error('WebSocket is not open.');
            }
        };

        recognition.onerror = (event) => {
            status.innerText = 'Speech recognition error: ' + event.error;
            isRecognitionActive = false;
            clearTimeout(recognitionTimeout);
        };

        recognition.onend = () => {
            console.log('response from ws:', reposne_from_ws)
            recognition.start();
            const timestamp = new Date().toLocaleString();
            console.log('ended', timestamp);
            isRecognitionActive = false;
            clearTimeout(recognitionTimeout);
        };

        recognition.start();
    } else {
        status.innerText = 'Your browser does not support Web Speech API.';
    }
}

function displayText(text) {
    status.innerHTML = '';
    console.log('text:', text);
    let textArray = text.split('$');
    let qaBox = document.createElement('div');
    qaBox.classList.add('qa-box');
    let ul = document.createElement('ul');
    for (let i = 0; i < textArray.length; i++) {
        let li = document.createElement('li');

        let strong = document.createElement('strong');
        strong.innerText = i % 2 === 0 ? 'Question: ' : 'Answer: ';
        strong.style.fontSize = '22px';
        li.appendChild(strong);
        let textNode = document.createTextNode(textArray[i]);
        let span = document.createElement('span');
        span.style.fontSize = '22px'; // Set font size for text elements
        span.appendChild(textNode);
        li.appendChild(span);

        // Add a new line after each question
        // Add a new line after each question
        if (i % 2 === 0) {
            li.appendChild(document.createElement('br'));
        } else {
            // Add double block (two <br> elements) after each answer
            li.appendChild(document.createElement('br'));
            li.appendChild(document.createElement('br'));
        }
        ul.appendChild(li);
    }
    qaBox.appendChild(ul);
    status.appendChild(qaBox);


}

startButton.onclick = () => {
    //ws = new WebSocket('wss://aide-3ai.com/ws');
    ws = new WebSocket('ws://127.0.0.1:8000/ws');
    ws.onopen = () => {
        console.log('WebSocket connection opened.');

        startRecognition(myVar);
    };
    ws.onmessage = (event) => {
        reposne_from_ws = event.data
        displayText(event.data);
    };
    ws.onclose = () => {
        console.log('WebSocket connection closed.');
        // startRecognition();

    };
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};