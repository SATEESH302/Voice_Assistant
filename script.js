const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const status = document.getElementById('status');
let ws;
let isRecognitionActive = false;

if (window.hasOwnProperty('webkitSpeechRecognition')) {
    const SpeechRecognition = webkitSpeechRecognition;
    var recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = function() {
        isRecognitionActive = true;
        status.innerText = 'Speech recognition active.';
    };

    recognition.onresult = function(event) {
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
            ws.send(finalTranscript || interimTranscript);
            console.log('sending', finalTranscript || interimTranscript);
        } else {
            console.error('WebSocket is not open.');
        }

        // Update status with question and answer
        // status.innerText = `Question: ${finalTranscript || interimTranscript}\nAnswer: Processing...`;
    };

    recognition.onerror = function(event) {
        status.innerText = 'Speech recognition error: ' + event.error;
        isRecognitionActive = false;
    };

    recognition.onend = function() {
        const timestamp = new Date().toLocaleString();
        console.log('ended', timestamp);
        isRecognitionActive = false;
    };
} else {
    status.innerText = 'Your browser does not support Web Speech API.';
}

function startRecognition() {
    if (recognition && !isRecognitionActive) {
        recognition.start();
        startButton.style.display = 'none';
        stopButton.style.display = 'inline-block';
    }
}

function stopRecognition() {
    if (recognition && isRecognitionActive) {
        recognition.stop();
        startButton.style.display = 'inline-block';
        stopButton.style.display = 'none';
    }
}

// WebSocket connection setup
ws = new WebSocket('wss://aide-3ai.com/ws');
ws.onopen = () => {
    console.log('WebSocket connection opened.');
};
ws.onmessage = (event) => {
    // speakText(event.data);
    displayText(event.data);    
};
ws.onclose = () => {
    console.log('WebSocket connection closed.');
};
ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

function displayText(text) {
    // Function to display text received from WebSocket
    // status.innerHTML = `${text}`;
    // split the text based on $ and assign even H1 for even index and H2 for odd index
    status.innerHTML = '';

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