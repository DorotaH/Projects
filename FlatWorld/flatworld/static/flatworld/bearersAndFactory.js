import {getCookie} from './flatworld.js';

document.addEventListener('DOMContentLoaded', function() {
    let generateFactory = document.getElementById('generateFactory');
    let generateBearers = document.getElementById('generateBearers');
    if (generateFactory) {
        generateFactory.addEventListener('click', factory);
    }
    if (generateBearers) {
        generateBearers.addEventListener('click', bearers);
    }
    window.addEventListener('message', function(event) {
        console.log('Received message: ', event.data);
    });
});

let globalfactory = false;
let globalbearers = false;

function factory() {
    fetch('./', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.message === 'Fabryka poza granicami świata') {
            factory();
        }
        let h3 = document.createElement('h3');
        h3.innerHTML = 'Fabryka powstała w punkcie: <span class="green-text">' + result.factory + '</span>';
        let page = document.getElementById('uno');
        page.appendChild(h3);
        document.getElementById('generateFactory').remove();
        globalfactory = true;
        check();
    });
}


function bearers() {
    const inputPoints = document.getElementById('inputPoints').value;
    if (inputPoints < 7) {
        alert('Podaj liczbe noszacych wieksza niz 7');
        return;
    }
    fetch('./bearers/', {
        method: 'POST',
        body: JSON.stringify({ inputPoints: inputPoints }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then( response => {return response.json(); })
    .then(result => {
        let h3 = document.createElement('h3');
        let p = document.createElement('p');
        let page = document.getElementById('dos');
        h3.innerHTML = 'Łącznie powstało: <span class="green-text">' + result.pairs + '</span> par tragarzy';
        page.appendChild(h3);
        document.getElementById('generateBearers').remove();
        document.getElementById('inputPoints').remove();
        document.getElementById('text').remove();
        globalbearers = true;
        check();
    }); 
}

function check() {
    if (globalfactory && globalbearers) {
        let button = document.createElement('button');
        button.innerHTML = 'Kontynuuj';
        button.addEventListener('click', function() {
            window.location.href = '/fence/';
        });
        let page = document.getElementById('main');
        page.appendChild(button);
    }
}
