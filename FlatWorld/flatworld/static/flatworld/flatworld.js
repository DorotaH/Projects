export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('reset').addEventListener('click', popup);
    let form = document.getElementById('confirmation');
    if (form) {
        form.addEventListener('click', popup);
    }
});

function popup(event) {
    event.preventDefault();
    fetch('/reset', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json', }
        })
        .then(response => { return response.json(); })
        .then(data => {
            let windowPopup;
            let overlay;
            if (data.adventure_exists === false){
                ({ windowPopup, overlay } = createPopup("Nie rozpocząłeś jeszcze przygody."));
                windowPopup.style.zIndex = 1001;
                let OKButton = document.createElement("button");
                OKButton.textContent = "Ok";
                OKButton.addEventListener('click', function() {
                    document.body.removeChild(windowPopup);
                    document.body.removeChild(overlay);
                    return;
                });
                windowPopup.appendChild(OKButton);
                document.body.appendChild(windowPopup);
                document.body.appendChild(overlay);
                return;
            } else {
                ({ windowPopup, overlay } = createPopup("Czy na pewno chcesz usunąć wszystkie dane? Wszystkie postępy zostaną utracone."));
                windowPopup.style.zIndex = 1001;

                let yesButton = document.createElement("button");
                yesButton.textContent = "Yes";
                let noButton = document.createElement("button");
                noButton.textContent = "No";

                yesButton.addEventListener('click', function() {
                    fetch('/reset/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        }
                    })
                    .then(response => { return response.json(); })
                    .then(data => {
                        document.body.removeChild(windowPopup);
                        ({ windowPopup, overlay } = createPopup(data.message));
                        windowPopup.style.zIndex = 1001;
                        document.body.appendChild(windowPopup);
                        setTimeout(function() {
                            window.location.href = '/';
                        }, 1000);
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
        });
    
}

export function createPopup(message) {
    let windowPopup = document.createElement("div");
    windowPopup.className = "popup";

    let text = document.createElement("p");
    text.textContent = message;
    windowPopup.appendChild(text);
    let overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = 0;
    overlay.style.left = 0;
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    overlay.style.zIndex = 1000;

    return { windowPopup, overlay };
}

