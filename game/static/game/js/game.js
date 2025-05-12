// Initialize game
function initGame() {
    if (gameState.timeLeft > 0) {
        startTimer();
    }
    setupEventListeners();
}

function startTimer() {
    gameState.timer = setInterval(() => {
        gameState.timeLeft--;
        elements.timer.textContent = gameState.timeLeft;
        
        if (gameState.timeLeft <= 0) {
            clearInterval(gameState.timer);
            handleTimeUp();
        }
    }, 1000);
}

function setupEventListeners() {
    elements.userCommand.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !gameState.isGameOver) {
            submitAnswer();
        }
    });
}

async function submitAnswer() {
    if (gameState.isGameOver) return;
    
    const command = elements.userCommand.value.trim();
    if (!command) return;

    disableInput();
    
    try {
        const response = await fetch('/validate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': gameState.csrfToken
            },
            body: JSON.stringify({
                question_id: document.getElementById('question_id').value,
                user_command: command,
                current_time: gameState.timeLeft
            })
        });
        
        const data = await response.json();
        handleResponse(data);
    } catch (error) {
        console.error('Error:', error);
        showFeedback("An error occurred", 'error');
        enableInput();
    }
}

function handleResponse(data) {
    if (data.result === 'correct') {
        handleCorrectAnswer(data);
    } else if (data.result === 'incorrect') {
        handleIncorrectAnswer(data);
    } else if (data.result === 'game_over') {
        handleGameOver(data);
    }
}

function handleCorrectAnswer(data) {
    console.log('Correct');
    showFeedback('Correct!', 'success');
    setTimeout(() => {
        location.reload();
    }, 1000);
    
}

function handleIncorrectAnswer(data) {
    console.log('Incorrect');
    showFeedback('Incorrect!', 'incorrect');
    if (elements.lives && data.lives !== undefined) {
        elements.lives.textContent = data.lives;
    }
    setTimeout(() => {
        elements.userCommand.value = '';
        enableInput();
    }, 1000);
}

function handleGameOver(data) {
    gameState.isGameOver = true;
    clearInterval(gameState.timer);
    elements.feedback.style.display = 'none';
    elements.gameOverMsg.style.display = 'block';
    if (elements.lives) {
        elements.lives.textContent = '0';
    }
    disableInput();
    
    setTimeout(() => {
        location.href = '/game_over/';
    }, 2000);
}

function handleTimeUp() {
    fetch('/time_up/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': gameState.csrfToken
        },
        body: JSON.stringify({ current_time: gameState.timeLeft })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'game_over') {
            handleGameOver(data);
        }
    })
    .catch(console.error);
}

function disableInput() {
    elements.userCommand.disabled = true;
}

function enableInput() {
    elements.userCommand.disabled = false;
    elements.userCommand.focus();
}

function showFeedback(message, type) {
    elements.feedback.textContent = message;
    elements.feedback.className = `feedback ${type}`;
    elements.feedback.style.display = 'block';
}


