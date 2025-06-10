document.addEventListener('DOMContentLoaded', () => {
    const chapterTitleElem = document.querySelector('.chapter-description h2');
    const chapterDescElem = document.querySelector('.chapter-description p');
    const missionDialogueElem = document.querySelector('.tux-dialogue');
    const taskDescElem = document.querySelector('.task-description');
    const taskIdInput = document.getElementById('task_id');
    const feedbackElem = document.getElementById('feedback');

    let currentMissionId = null;
    let mistakeCount = 0;
    let currentHints = [];
    let feedbackTimeout = null;

    async function fetchStoryModeData() {
        try {
            const response = await fetch('/story_mode_data/');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();

            if (data.chapter) {
                chapterTitleElem.textContent = data.chapter.name || 'No Chapter Name';
                chapterDescElem.textContent = data.chapter.description || '';
            } else {
                chapterTitleElem.textContent = 'No Chapter';
                chapterDescElem.textContent = '';
            }

            if (data.mission) {
                missionDialogueElem.textContent = data.mission.instructor_sentence || '';
                currentMissionId = data.mission.id || null;
            } else {
                missionDialogueElem.textContent = '';
                currentMissionId = null;
            }

            if (data.task) {
                taskDescElem.textContent = data.task.task || '';
                taskIdInput.value = data.task.id || '';
                currentHints = data.task.hints || [];
            } else {
                taskDescElem.textContent = '';
                taskIdInput.value = '';
                currentHints = [];
            }
            mistakeCount = 0; // reset mistake count on new task
            clearFeedback();
        } catch (error) {
            console.error('Failed to fetch story mode data:', error);
            showFeedback('Failed to load story data.', false, true);
        }
    }

    function showFeedback(message, isHint = false, isPersistent = false) {
        if (feedbackTimeout) {
            clearTimeout(feedbackTimeout);
            feedbackTimeout = null;
        }
        feedbackElem.textContent = message;
        if (isHint) {
            feedbackElem.style.color = 'orange';
        } else {
            feedbackElem.style.color = 'green';
        }
        if (!isPersistent) {
            // Clear feedback after 3 seconds
            feedbackTimeout = setTimeout(() => {
                clearFeedback();
            }, 3000);
        }
    }

    function clearFeedback() {
        feedbackElem.textContent = '';
        feedbackElem.style.color = '';
        if (feedbackTimeout) {
            clearTimeout(feedbackTimeout);
            feedbackTimeout = null;
        }
    }

    async function validate_sm_command() {
        const userCommandInput = document.getElementById('user_command');
        const userCommand = userCommandInput.value.trim();
        const taskId = taskIdInput.value;

        if (!userCommand) {
            showFeedback('Please enter a command.');
            return;
        }
        if (!taskId) {
            showFeedback('Task ID is missing.');
            return;
        }
        if (!currentMissionId) {
            showFeedback('Mission ID is missing.');
            return;
        }

        try {
            // Fetch correct commands from validate_sm endpoint
            const validateResponse = await fetch('/validate_sm/');
            if (!validateResponse.ok) {
                throw new Error('Failed to validate command');
            }
            const validateData = await validateResponse.json();
            const correctCommands = validateData.correct_commands || [];

            // Check if user command matches any correct command (case-insensitive)
            const isCorrect = correctCommands.some(cmd => cmd.trim().toLowerCase() === userCommand.toLowerCase());

            if (isCorrect) {
                // Call complete_mission endpoint with mission_id
                const completeResponse = await fetch('/complete_mission/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ mission_id: currentMissionId }),
                });

                if (!completeResponse.ok) {
                    throw new Error('Failed to complete mission');
                }

                const completeData = await completeResponse.json();

                // Update UI with success message and load next mission data if available
                showFeedback('Correct! Mission completed. Loading next mission...', false, true);

                // Refetch all story mode data to update UI dynamically
                await fetchStoryModeData();

                userCommandInput.value = '';
            } else {
                mistakeCount++;
                userCommandInput.value = '';
                if (mistakeCount >= 2 && currentHints.length > 0) {
                    // Calculate hint index based on mistakeCount (start showing from 2 mistakes)
                    let hintIndex = mistakeCount - 2;
                    if (hintIndex >= currentHints.length) {
                        hintIndex = currentHints.length - 1; // show last hint if out of range
                    }
                    showFeedback('Hint: ' + currentHints[hintIndex], true);
                } else {
                    showFeedback('Incorrect command. Please try again.', false, true);
                }
            }
        } catch (error) {
            console.error('Error during command validation:', error);
            showFeedback('An error occurred during validation. Please try again.', false, true);
        }
    }

    // Helper function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Expose validate_sm_command globally so it can be called from inline onkeydown
    window.validate_sm_command = validate_sm_command;

    fetchStoryModeData();
});
