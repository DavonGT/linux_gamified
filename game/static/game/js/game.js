// Initialize game
function initGame() {
    if (gameState.timeLeft > 0) {
        startTimer();
    }
    setupEventListeners();
}

// Initialize modal elements after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('giveUpModal');
    const closeButtons = document.querySelectorAll('.close-modal');

    // Close modal when clicking the close button
    function closeModal() {
        modal.style.display = 'none';
    }

    closeButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });

    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Show give up modal
    window.showGiveUpModal = () => {
        modal.style.display = 'block';
    }
});

// Handle give up confirmation
async function confirmGiveUp() {
    // Clean up game state
    gameState.isGameOver = true;
    clearInterval(gameState.timer);
    disableInput();
    
    // Show game over message with fade effect
    elements.feedback.style.display = 'none';
    elements.gameOverMsg.style.display = 'block';
    elements.gameOverMsg.style.opacity = '0';
    
    // Fade in game over message
    setTimeout(() => {
        elements.gameOverMsg.style.opacity = '1';
    }, 100);
    
    // Navigate to game over page after a brief delay
    setTimeout(() => {
        window.location.href = "/game_over/";
    }, 1000);
    
    // Close the modal
    closeModal();
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
        location.reload();
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


