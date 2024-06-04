document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      console.log(email);
      const email_div = document.createElement('div');
      const inner_div = document.createElement('div');
      inner_div.innerHTML = `
        <div style="display: flex; justify-content: space-between;">
          <p style="text-align: left;"><strong>${email.sender}</strong>
          &nbsp&nbsp${email.subject}</p>
          <p style="text-align: right; color: grey">${email.timestamp}</p>
        </div>
      `.replace(/\n/g, '');
      inner_div.addEventListener('click', () => read_email(email.id));
      inner_div.style.outline = '1px solid black';
      if (email.read) {
        inner_div.style.backgroundColor = 'lightgray';
      }
      email_div.appendChild(inner_div);
      document.querySelector('#emails-view').append(email_div);
    });
  });
}

function send_email(event) {
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const body = document.querySelector('#compose-body').value;
  const subject = document.querySelector('#compose-subject').value;
  if (recipients === '' || body === '' || subject === '') {
    alert(`Please fill all fields`);
    return;
  }
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result.error === `User with email ${recipients} does not exist.`) {
      alert(result.error);
      return;
    } else {
      load_mailbox('sent');
      alert(`e-mail to ${recipients} succesfully sent`);
    }
  }); 
}

function read_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#emails-view').innerHTML = '';

    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });

    const email_div = document.createElement('div');
    email_div.innerHTML = `
      <p><strong>From:</strong> ${email.sender}</p>
      <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
      <p><strong>Subject:</strong> ${email.subject}</p>
      <p><strong>Timestamp:</strong> ${email.timestamp}</p>
      <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
      <hr>
      <p>${email.body}</p>
    `;
  document.querySelector('#emails-view').append(email_div);
  document.querySelector('#reply').addEventListener('click', () => reply_to_email(email.id));

  const archive_button = document.createElement('button');
  archive_button.className = email.archived ? 'btn btn-sm btn-outline-success' : 'btn btn-sm btn-outline-danger';
  archive_button.innerHTML = email.archived ? 'Unarchive' : 'Archive';
  document.querySelector('#emails-view').append(archive_button);
  archive_button.addEventListener('click', function() {
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !email.archived
      })
    })
    .then(result => {
    load_mailbox('inbox');
  }); 
  });
  
  });
}

function reply_to_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Fill in composition fields
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    document.querySelector('#compose-body').value = 'On ' + email.timestamp + ' ' + email.sender + ' wrote: ' + email.body;
  });
}