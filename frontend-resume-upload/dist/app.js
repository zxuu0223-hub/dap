const input = document.querySelector('#resume-input');
const zone = document.querySelector('#drop-zone');
const fileState = document.querySelector('#file-state');
const fileName = document.querySelector('#file-name');
const fileSize = document.querySelector('#file-size');
const removeButton = document.querySelector('#remove-file');
const finishButton = document.querySelector('#finish');
const error = document.querySelector('#error-message');

const accepted = new Set([
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
]);

function readableSize(bytes) {
  return bytes < 1024 * 1024 ? `${Math.ceil(bytes / 1024)} KB` : `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function clearFile() {
  input.value = '';
  fileState.hidden = true;
  finishButton.disabled = true;
  error.textContent = '';
}

function useFile(file) {
  clearFile();
  if (!file) return;
  const extensionAllowed = /\.(pdf|doc|docx)$/i.test(file.name);
  if (!(accepted.has(file.type) || extensionAllowed)) {
    error.textContent = 'Please select a PDF, DOC, or DOCX resume.';
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    error.textContent = 'The selected file is larger than 10 MB.';
    return;
  }
  fileName.textContent = file.name;
  fileSize.textContent = `${readableSize(file.size)} · Ready to upload`;
  fileState.hidden = false;
  finishButton.disabled = false;
}

input.addEventListener('change', () => useFile(input.files[0]));
zone.addEventListener('keydown', event => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    input.click();
  }
});
['dragenter', 'dragover'].forEach(name => zone.addEventListener(name, event => {
  event.preventDefault();
  zone.classList.add('dragging');
}));
['dragleave', 'drop'].forEach(name => zone.addEventListener(name, event => {
  event.preventDefault();
  zone.classList.remove('dragging');
}));
zone.addEventListener('drop', event => useFile(event.dataTransfer.files[0]));
removeButton.addEventListener('click', clearFile);
finishButton.addEventListener('click', () => {
  finishButton.textContent = 'Uploaded ✓';
  finishButton.disabled = true;
});
document.querySelector('#previous').addEventListener('click', () => history.back());
