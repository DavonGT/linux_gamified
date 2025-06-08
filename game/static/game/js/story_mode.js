initTerminals();

writeStatic("Welcome to Story Mode!");

async function getData() {
  try {
    const res = await fetch('/story_mode_data/');
    const data = await res.json();

    if (data.chapter) {
      await writeTyped(`Chapter: ${data.chapter.name}`);
      await writeTyped(`Description: ${data.chapter.description}`);
    }
    if (data.mission) {
      await writeTyped(`Mission: ${data.mission.name}`);
    }
    if (data.task) {
      await writeTyped(`Task: ${data.task.task}`);
    }
  } catch (err) {
    writeStatic("Failed to fetch story data.");
  }
}

getData();

onInputKey(input => {
  writeStatic('> ' + input);
});
