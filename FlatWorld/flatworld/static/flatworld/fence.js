import {getCookie} from './flatworld.js';
import {createPopup} from './flatworld.js';

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generateFence').addEventListener('click', fence);
    let seeNeighbors = this.getElementById('showTable');
    if(seeNeighbors){
        seeNeighbors.addEventListener('click', neighbors);
    }
});

function fence(){
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search.slice(1));

    params.append('fence', '');

    url.search = params.toString();

    fetch(url)
    .then(response => response.json())
    .then(data =>{
        

        document.getElementById('generateFence').remove();
        
    })
    .catch(error => console.error('Error:', error));
}


function neighbors(){
    let windowPopup, overlay;
    ({ windowPopup, overlay } = createPopup("Lista sąsiadów"));
    windowPopup.style.zIndex = 1001;
    windowPopup.style.width = '100%'; // Increase the width of the popup to full width
    windowPopup.style.maxWidth = '50%'; // Increase the maximum width to full width
    windowPopup.style.display = 'flex'; // Add this line
    windowPopup.style.justifyContent = 'center'; // Add this line
    windowPopup.style.alignItems = 'center'; // Add this line

    // Get the table data
    let table = document.getElementById('neighborsTable').cloneNode(true);

    // Make the table visible
    table.style.display = 'table';

    // Add the table to the popup
    windowPopup.appendChild(table);
    document.body.appendChild(overlay);

    document.body.appendChild(windowPopup);

    // Add click event to overlay
    overlay.addEventListener('click', function() {
        // Remove the popup and overlay
        document.body.removeChild(windowPopup);
        document.body.removeChild(overlay);
    });
}