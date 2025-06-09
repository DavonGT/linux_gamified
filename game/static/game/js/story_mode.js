initTerminals();

writeStatic("Welcome to Story Mode!");

let currentMissionId = null;
let hintIndex = 0;
let incorrectCount = 0;  // Track number of incorrect responses

async function getData() {
  try {
    const res = await fetch('/story_mode_data/');
    const data = await res.json();

    if (data.chapter) {
      typedTerm.writeln(`\r\n\x1b[36mChapter:\x1b[0m ${data.chapter.name}`);
      typedTerm.writeln(`\x1b[36mDescription:\x1b[0m ${data.chapter.description}`);
    }
    if (data.mission) {
      currentMissionId = data.mission.id;
      await writeTyped(`\x1b[36mTux:\x1b[0m ${data.mission.instructor_sentence}`);
    }
    if (data.task) {
      typedTerm.writeln(`\r\n\x1b[36mTask:\x1b[0m ${data.task.task}`);
      // typedTerm.writeln(`\x1b[36mHint:\x1b[0m ${data.task.hints[hintIndex]}`);
    }
  } catch (err) {
    writeStatic("\r\n\x1b[31mFailed to fetch story data.\x1b[0m");
  }
}

async function completeMission() {
  try {
    const res = await fetch('/complete_mission/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ mission_id: currentMissionId })
    });
    const data = await res.json();

    if (data.next_mission) {
      currentMissionId = data.next_mission.id;
      hintIndex = 0;
      incorrectCount = 0;  // Reset incorrect count on new mission
      staticTerm.reset();
      writeStatic("\r\n\x1b[32mMission completed! Loading next mission...\x1b[0m");
      await getData();
    } else {
      staticTerm.reset();
      writeStatic("\r\n\x1b[32mCongratulations! You have completed all missions.\x1b[0m");
    }
  } catch (err) {
    writeStatic("\r\n\x1b[31mFailed to complete mission.\x1b[0m");
  }
}

async function check_command(user_command){
  try {
    const res = await fetch('/validate_sm/'); 
    const data = await res.json();

      if (data.correct_commands){
        if (data.correct_commands.includes(user_command)){
          await writeTyped("\r\n\x1b[32mCorrect!\x1b[0m");
          await new Promise(resolve => setTimeout(resolve, 500));  // Wait 0.5 seconds
          typedTerm.reset();
          await completeMission();
        }
        else{
          incorrectCount++;  // Increment incorrect count
          await writeTyped("\r\n\x1b[31mIncorrect!\x1b[0m");
        }
      }
  }
  catch (err){  
    writeStatic("\r\n\x1b[31mFailed to check your command. Reload the page\x1b[0m");
  }
}

getData();

onInputKey(async input => {
  if (input === 'clear'){
      staticTerm.reset();
      writeStatic('\r\n\x1b[36mWelcome to Story Mode!\x1b[0m');
      inputTerm.write('> ');
  }
  else if (input === 'hint'){
      if (incorrectCount >= 2){
          // Show hint if available
          const res = await fetch('/story_mode_data/');
          const data = await res.json();
          if (data.task && data.task.hints && hintIndex < data.task.hints.length){
              staticTerm.writeln(`\r\n\x1b[33mHint:\x1b[0m ${data.task.hints[hintIndex]}`);
              hintIndex++;
          } else {
              staticTerm.writeln(`\r\n\x1b[33mNo more hints available.\x1b[0m`);
          }
      } else {
          staticTerm.writeln(`\r\n\x1b[33mHint command is only available after 2 incorrect responses.\x1b[0m`);
      }
  }
  else if (input !== 'clear'){
      writeStatic('\r\n> ' + input);
      await check_command(input);
  }
  else {
    writeStatic('\r\n> ' + input);
  }
});
