(() => {
  const windowBar = document.getElementById('window-bar');
  ['close', 'minimize', 'maximize'].forEach(cls => {
    const circle = document.createElement('div');
    circle.classList.add('circle', cls);
    windowBar.appendChild(circle);
  });
})();
