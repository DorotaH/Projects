import {getCookie} from './flatworld.js';
import {createPopup} from './flatworld.js';

document.addEventListener('DOMContentLoaded', function() {
    let button = document.getElementById('generateCode');
    if(button){
        button.addEventListener('click', code);
    }
    let additionalbutton = document.getElementById('generateNewCode');
    if(additionalbutton){
        additionalbutton.addEventListener('click', customcode);
    }
});

function code(){
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search.slice(1));

    params.append('code', '');

    url.search = params.toString();

    fetch(url)
    .then(response => response.json())
    .then(data =>{
        print(data);
    });
}

function customcode(){
    fetch('./', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'song_to_code': document.getElementById('inputText').value
        })
    })
    .then(response => response.json())
    .then(data =>{
        print(data);
    });
}

function print(data){
    let code = data.code;
    let uncoded_song = data.uncoded_song;
    let coded_song = data.coded_song;
    let page = document.querySelector('.page');
    let leftpage = document.getElementById('left');
    let rightpage = document.getElementById('right');
    let h3Element1 = document.createElement('h3');
    h3Element1.style.wordBreak = 'break-all';
    h3Element1.innerHTML = "Zakodowana piosenka brzmi: " + coded_song;
    h3Element1.className = 'borderPage';

        let table = document.createElement('table');
        let thead = document.createElement('thead');
        let tbody = document.createElement('tbody');

        let headerRow = document.createElement('tr');
        let th1 = document.createElement('th');
        th1.textContent = "Klucz";
        let th2 = document.createElement('th');
        th2.textContent = "Wartość";
        headerRow.appendChild(th1);
        headerRow.appendChild(th2);
        thead.appendChild(headerRow);
        table.appendChild(thead);

        for (let key in code) {
            let row = document.createElement('tr');
            let td1 = document.createElement('td');
            let td2 = document.createElement('td');
        
            if (key === ' ') {
                td1.textContent = '" "';
            } else if (key === '\n') {
                td1.textContent = '"\\n"';
            } else {
                td1.textContent = key;
            }
        
            td2.textContent = code[key];
            row.appendChild(td1);
            row.appendChild(td2);
            tbody.appendChild(row);
        }
        table.appendChild(tbody);

        leftpage.appendChild(table);

        let h3Element3 = document.createElement('h3');
        h3Element3.innerHTML = "Informatyk od razu próbował odkodować piosenkę, sprawdź czy wyszło mu to co zakodował! <br>" + uncoded_song;
        rightpage.appendChild(h3Element3);
        rightpage.appendChild(h3Element1);

        
        document.getElementById('text1').remove();
        document.getElementById('text2').remove();
        document.getElementById('inputText').remove();
        document.getElementById('generateNewCode').remove();
        document.getElementById('generateCode').remove();
        
}

