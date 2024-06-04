import {createPopup} from './flatworld.js';
import {getCookie} from './flatworld.js';

document.addEventListener('DOMContentLoaded', function() {
    let buttons = document.querySelectorAll('.btn');
    if (buttons) {
        buttons.forEach((button) => {
            button.addEventListener('click', change);
        });
    }
});

function change() {
    let windowPopup, overlay;
    ({ windowPopup, overlay } = createPopup("Czy to jest słowo, które zostało zmienione?"));
    windowPopup.style.zIndex = 1001;

    let yesButton = document.createElement("button");
    yesButton.textContent = "Yes";
    let noButton = document.createElement("button");
    noButton.textContent = "No";
    let word_to_change = this.textContent;
    yesButton.addEventListener('click', function() {
        fetch('./', {
            method: 'POST',
            body: JSON.stringify({ 'word_to_change': word_to_change }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            document.body.removeChild(windowPopup);
            document.body.removeChild(overlay);
            let indexes = data.indexes;
            let word_indexes = data.word_indexes;
            let new_song = data.changed_song;
            let changed_word = data.changed_word;
            document.getElementById('menu').remove();
            let h3 = document.createElement('h3');
            let h32 = document.createElement('h3');
            h32.className = 'borderPage';
            h32.style.wordWrap = 'break-word';
            h3.textContent = "Zmieniono słowo na indeksach LITER: " + indexes + "\nSą to SŁOWA o indeksach: " + word_indexes;
            let words = new_song.split(/\s+/);
            for (let i = 0; i < words.length; i++) {
                if ((i+1) % 5 === 0) {
                    words[i] = words[i] + ' <br>';
                } else if(words[i].trim() === changed_word.trim()) {
                    words[i] = `<span style="color:green;">${words[i]}</span>`;
                }
            }
            new_song = words.join(' ');
            h32.innerHTML = "Nowa piosenka: <br>" + new_song;
        
            let page = document.querySelector('.page');
            
            page.appendChild(h3);
            page.appendChild(h32);
        });
    });

    noButton.addEventListener('click', function() {
        document.body.removeChild(windowPopup);
        document.body.removeChild(overlay);
    });

    windowPopup.appendChild(yesButton);
    windowPopup.appendChild(noButton);
    document.body.appendChild(windowPopup);
    document.body.appendChild(overlay);
}