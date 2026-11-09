// Turns <form data-mailto="address" data-subject="..."> into a pre-filled e-mail.
// GitHub Pages cannot send e-mails itself, so the visitor's mail app opens with the message ready to send.
// Every field to include needs a data-label attribute; ticked checkboxes are listed by their label.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form[data-mailto]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const lines = [];
      form.querySelectorAll('[data-label]').forEach((field) => {
        if (field.type === 'checkbox') {
          if (field.checked) lines.push('- ' + field.dataset.label);
          return;
        }
        const value = field.value.trim();
        if (value) lines.push(field.dataset.label + ' : ' + value);
      });
      window.location.href = 'mailto:' + form.dataset.mailto +
        '?subject=' + encodeURIComponent(form.dataset.subject || '') +
        '&body=' + encodeURIComponent(lines.join('\n'));
      const note = form.querySelector('.mailto-note');
      if (note) note.hidden = false;
    });
  });
});
