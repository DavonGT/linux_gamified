let typedTerm, staticTerm, inputTerm;
let typedFit, staticFit, inputFit;

function initTerminals() {
  typedTerm = new Terminal({
    convertEol: true,
    wordWrap: true,
    cursorBlink: false,
    theme: {
      background: '#121214',
      foreground: '#e0e0e0',
      cursor: '#f5f5f7',
    }
  });
  typedFit = new window.FitAddon.FitAddon();
  typedTerm.loadAddon(typedFit);
  typedTerm.open(document.getElementById('typed-terminal'));
  typedFit.fit();

  staticTerm = new Terminal({ 
    convertEol: true,
    wordWrap: true,
    cursorBlink: false,
    theme: {
      background: '#121214',
      foreground: '#e0e0e0',
      cursor: '#f5f5f7',
    }
   });
  staticFit = new window.FitAddon.FitAddon();
  staticTerm.loadAddon(staticFit);
  staticTerm.open(document.getElementById('static-terminal'));
  staticFit.fit();

  inputTerm = new Terminal({ 
    cursorBlink: true,
    disableStdin: false,
    rows: 1,
    theme: {
      background: '#121214',
      foreground: '#e0e0e0',
      cursor: '#f5f5f7',
    }
  });
  inputFit = new window.FitAddon.FitAddon();
  inputTerm.loadAddon(inputFit);
  inputTerm.open(document.getElementById('input-terminal'));
  inputFit.fit();

  window.addEventListener('resize', () => {
    typedFit.fit();
    staticFit.fit();
    inputFit.fit();
  });
  inputTerm.focus();
}

function writeStatic(text) {
  staticTerm.writeln(text);
}

function writeTyped(text, delay = 20) {
  return new Promise(resolve => {
    let i = 0;
    function typeChar() {
      if (i < text.length) {
        typedTerm.write(text[i++]);
        setTimeout(typeChar, delay);
      } else {
        typedTerm.write('\r\n');
        resolve();
      }
    }
    typeChar();
  });
}

function onInputKey(callback) {
  let inputBuffer = '';
  inputTerm.write('> ');
  inputTerm.onKey(e => {
    const key = e.key;
    if (key === '\r') {
      callback(inputBuffer);
      inputBuffer = '';
      inputTerm.reset();
      inputTerm.write('> ');
    } else if (key === '\u007F') {
      if (inputBuffer.length > 0) {
        inputBuffer = inputBuffer.slice(0, -1);
        inputTerm.write('\b \b');
      }
    } else {
      inputBuffer += key;
      inputTerm.write(key);
    }
  });
}
