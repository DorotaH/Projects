import {getCookie} from './flatworld.js';

document.addEventListener('DOMContentLoaded', function() {
    let buttonSmall = document.getElementById('generateSmallWorld');
    let buttonMedium = document.getElementById('generateMediumWorld');
    let buttonBig = document.getElementById('generateBigWorld');
    let buttonCustom = document.getElementById('customWorld');
    if (buttonSmall) {
        buttonSmall.addEventListener('click', function() {
            small = true;
            medium = false;
            big = false;
            custom = false;
            generateWorld();
        });
    }
    if (buttonMedium) {
        buttonMedium.addEventListener('click', function() {
            small = false;
            medium = true;
            big = false;
            custom = false;
            generateWorld();
        });
    }
    if (buttonBig) {
        buttonBig.addEventListener('click', function() {
            small = false;
            medium = false;
            big = true;
            custom = false;
            generateWorld();
        });
    }
    if (buttonCustom) {
        buttonCustom.addEventListener('click', function() {
            small = false;
            medium = false;
            big = false;
            custom = true;
            generateWorld();
        });
    }
});
let small = false;
let medium = false;
let big = false;
let custom = false;

function generateWorld(){
    let inputPoints;
    if (small) {
        inputPoints = Math.floor(Math.random() * (10 - 5 + 1)) + 5;
    }
    if (medium) {
        inputPoints = Math.floor(Math.random() * (20 - 10 + 1)) + 10;
    }
    if (big) {
        inputPoints = Math.floor(Math.random() * (50 - 20 + 1)) + 20;
    }
    if (custom) {
        inputPoints = document.getElementById('inputPoints').value;
    }
    fetch('./', {
        method: 'POST',
        body: JSON.stringify({inputPoints: inputPoints}),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(image => {
        const img = document.createElement('img'); 
        img.src = image.world_url;
        const pageElement = document.querySelector('.page');
        img.style.width = '800px';
        pageElement.appendChild(img); 
        img.onload = () => console.log('Image loaded');
        img.onerror = () => console.log('Image load error');

        document.getElementById('generateSmallWorld').remove();
        document.getElementById('generateMediumWorld').remove();
        document.getElementById('generateBigWorld').remove();
        document.getElementById('inputPoints').remove();
        document.getElementById('customWorld').remove();
        document.getElementById('inputPointsGenerated2').remove();
        document.getElementById('inputPointsGenerated1').innerHTML = 'Kraina zostala wygenerowana z ' + inputPoints + ' punktow';
        const div = document.createElement('div');
        const h3 = document.createElement('h3');
        const button = document.createElement('button');
        button.innerHTML = 'Kontynuuj';
        h3.innerHTML = 'Zauważyłeś, że po kartkach płynie pewna melodia.\n Szczerze? Brzydka, zmieniłbyś ją. dotykasz literek palcami i majstrujesz....'.replace(/\n/g, '<br>');
        div.appendChild(h3);  
        div.appendChild(button);
        pageElement.appendChild(div);
        button.addEventListener('click', function() {
            window.location.href = '/song/';
        });
    })
    .catch(error => console.error(error));
}
