(() => {
  const form = document.querySelector('.terminal-form');
  if (!form) return;

  const input = form.querySelector('.terminal-input');
  const output = document.querySelector('.terminal-output');
  const history = output.querySelector('.terminal-history');
  let outputTimer;

  const clearOutput = () => {
    history.replaceChildren();
    output.hidden = true;
  };

  input.addEventListener('input', () => {
    input.style.width = `${Math.max(1, Math.min(input.value.length + 1, 30))}ch`;
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const command = input.value.trim();
    if (!command) return;

    const normalized = command.replace(/\s+/g, ' ');
    input.value = '';
    input.style.width = '1ch';
    input.focus();
    if (!['ls', 'cat flag.txt', 'clear'].includes(normalized)) return;

    clearTimeout(outputTimer);
    if (normalized === 'clear') {
      clearOutput();
    } else {
      let response;
      if (normalized === 'ls') {
        response = 'flag.txt';
      } else if (normalized === 'cat flag.txt') {
        response = '축하합니다 flag를 얻으셨어요!';
      }

      const entry = document.createElement('li');
      const prompt = document.createElement('div');
      prompt.className = 'terminal-command';
      prompt.textContent = `$ ${command}`;
      const result = document.createElement('pre');
      result.textContent = response;
      entry.append(prompt, result);
      history.append(entry);
      while (history.children.length > 12) history.firstElementChild.remove();
      output.hidden = false;
      output.scrollTop = output.scrollHeight;
      outputTimer = setTimeout(clearOutput, 15000);
    }

  });
})();
