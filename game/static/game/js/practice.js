function showHint() {
    if (document.getElementById('hint').style.display === 'block') {
        document.getElementById('hint').style.display = 'none';
        return;
    }
    document.getElementById('hint').style.display = 'block';
}

function submitPracticeAnswer() {
    const questionId = document.getElementById('question_id').value;
    const userCommandInput = document.getElementById('user_command');
    const userCommand = userCommandInput.value.trim();

    if (!userCommand) {
        document.getElementById('feedback').textContent = 'Command cannot be empty!';
        document.getElementById('feedback').className = 'feedback incorrect';
        userCommandInput.focus();
        return;
    }

    userCommandInput.disabled = true;

    fetch('/validate_practice_answer/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ question_id: questionId, user_command: userCommand })
    })
    .then(response => response.json())
    .then(data => {
        const feedbackElement = document.getElementById('feedback');
        if (data.result === 'correct') {
            feedbackElement.textContent = 'Correct!';
            feedbackElement.className = 'feedback correct';
            setTimeout(() => window.location.reload(), 1000);
        } else {
            feedbackElement.textContent = 'Incorrect! Try again.';
            feedbackElement.className = 'feedback incorrect';
            userCommandInput.value = '';
            userCommandInput.disabled = false;
            userCommandInput.focus();
        }
    })
    .catch(() => {
        alert('An error occurred.');
        userCommandInput.disabled = false;
        userCommandInput.focus();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('user_command').focus();
});