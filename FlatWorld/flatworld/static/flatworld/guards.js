import {getCookie} from './flatworld.js';

document.addEventListener('DOMContentLoaded', function() {
    let generateGuards = document.getElementById('generateGuards');
    if (generateGuards) {
        generateGuards.addEventListener('click', schedule);
    }
});

function schedule(){
    let inputPoints = document.getElementById('inputPoints').value;
    if (inputPoints === '' || inputPoints < 2 || inputPoints > 20) {
        alert('Podaj liczbę punktów z zakresu 2-20.');
        return;
    }
    fetch('/guards/', {
        method: 'POST',
        body: JSON.stringify({ inputPoints: inputPoints }),
        headers: { 'Content-Type': 'application/json',      
                'X-CSRFToken': getCookie('csrftoken')}
    })
    .then(response => { return response.json(); })
    .then(data => {
        window.location.href = './';
    });
    /*.then(response => { return response.json(); })
    .then(data => {
        data.forEach((day, index) => {  
            let pageFlexElement = document.createElement('div');
            let page = document.createElement('div');
            page.className = "page";
            pageFlexElement.className = "pageFlex";

            let dividedPageElement1 = document.createElement('div');
            dividedPageElement1.className = "dividedPage";
            dividedPageElement1.innerHTML = `
                <h2> Dzień: <span class="green-text">${index+1}</span></h2>
                <h3> Id strażnika: <span class="green-text">${day.person_id}</span></h3>
                <h3> Punkty zatrzymania: <span class="green-text">${day.stop_points}</span> </h3>
                <h3> Miejsca odsłuchania piosenek: <span class="green-text">${day.songs}</span></h3>
                <h3> Ilość odsłuchania piosenki: <span class="green-text">${day.songs.length}</span></h3>
            `;

            let dividedPageElement2 = document.createElement('div');
            dividedPageElement2.className = "dividedPage";
            dividedPageElement2.innerHTML = `
                <img src="${day.image}" alt="">
            `;

            pageFlexElement.appendChild(dividedPageElement1);
            pageFlexElement.appendChild(dividedPageElement2);
            
            page.appendChild(pageFlexElement);
        document.body.appendChild(page);
        document.getElementById('generateGuards').remove();
        document.getElementById('inputPoints').remove();
        });
    });*/
}