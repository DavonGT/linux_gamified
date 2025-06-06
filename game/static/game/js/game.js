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

function preventBackspaceInHardcore(event) {
    // Check if the pressed key is backspace and if we're in a hardcore mode
    if ((event.key === 'Backspace' || event.keyCode === 8) && 
        (gameState.mode === 'hardcore_survival' || gameState.mode === 'hardcore_time_attack')) {
        event.preventDefault();
        return false;
    }
    return true;
}

function setupEventListeners() {
    elements.userCommand.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !gameState.isGameOver) {
            submitAnswer();
        }
        // Prevent backspace in hardcore modes
        if ((e.key === 'Backspace' || e.keyCode === 8) && 
            (gameState.mode === 'hardcore_survival' || gameState.mode === 'hardcore_time_attack')) {
            e.preventDefault();
            return false;
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
                task_id: document.getElementById('task_id').value,
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
    elements.feedback.innerHTML = message;
    elements.feedback.style.display = 'block';
}


