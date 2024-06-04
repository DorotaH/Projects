document.addEventListener('DOMContentLoaded', function() {
    load_follows();
    load_likes();

    var currentMode = localStorage.getItem('mode');
    if (currentMode === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    document.body.addEventListener('click', function(event) {
        if (event.target.matches('.edit')) {
            event.preventDefault();
            const postId = event.target.getAttribute('data-id');
            openModal(postId);
        }
    });

    document.getElementById('mode-toggle').addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');

        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('mode', 'dark');
        } else {
            localStorage.setItem('mode', 'light');
        }
    });
});

// ... rest of your code ...

function load_likes() {
    const likesElements = document.querySelectorAll('.likes');
    likesElements.forEach(likes => {
        const postID = likes.getAttribute('data-id'); 
        fetch(`/likes/${postID}`)
        .then(response => response.json())
        .then(data => {
            const postLikes = data.likes;
            const isLiked = data.is_liked;
            const is_authenticated = data.is_authenticated;
            const heart = document.createElement('p');
            heart.id = `heart${postID}`;
            heart.textContent = `${postLikes} Likes`;
            if (isLiked) {
                heart.style.color = 'red';
                heart.classList.add('fas', 'fa-heart', 'fa-1x');
                heart.dataset.liked = 'true';
            } else {
                heart.style.color = 'grey';
                heart.classList.add('far', 'fa-heart', 'fa-1x');
                heart.dataset.liked = 'false';
            }
            likes.appendChild(heart);
            if (is_authenticated)
                heart.onclick = () => manage_likes(postID, postLikes);
        });
    });
}

function load_follows() {
    const url = window.location.pathname;
    const isProfilePage = url.startsWith('/profile/');
    if (isProfilePage){
        fetch(`${url}follow/`)
        .then(response => response.json())
        .then(data => {
            const profile_user = data.username;
            const current_user = data.current_user;
            is_following = data.is_following;
            const socials_div = document.querySelector('#socials');
            const socials = document.createElement('p');
            socials.innerHTML = `following: ${data.following} followers: ${data.followers}`;
            socials_div.appendChild(socials);
            if (current_user !== profile_user && current_user !== null) {
                const followBtn = document.createElement('button');
                followBtn.id = 'follow-btn';
                followBtn.className = 'btn btn-primary';
                followBtn.textContent = is_following ? 'Unfollow' : 'Follow';
                socials_div.appendChild(followBtn);
                followBtn.addEventListener('click', function() {
                    fetch(`${url}follow/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({
                            username: followBtn.textContent.toLowerCase()
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        followBtn.textContent = data.is_following ? 'Unfollow' : 'Follow';
                        socials.innerHTML = `following: ${data.following} followers: ${data.followers}`;
                    })
                });
            }});
        
    }
}

function openModal(post_id) {
    const modal = document.createElement('div');
    modal.id = `modal${post_id}`;
    modal.className = 'modal';
    fetch(`/edit/${post_id}`, {method: 'GET' })
    .then(response => response.json())
    .then(data => {
        const post = data.post;
        let content = post.content;
        modal.innerHTML = `
            <div class="form-group">
                <textarea class="area" id="new-content" maxlength="150" rows = "7">${content}</textarea>
            </div>
            <button type="submit" id="edit-button" class="btn btn-primary">Submit</button>
        `;
        document.body.appendChild(modal);
        document.getElementById('edit-button').addEventListener('click', function(event) {
            event.preventDefault();
            const new_content = document.getElementById('new-content').value;
            fetch(`/edit/${post_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    content: new_content
                })
            })
            .then(response => response.json())
            .then(data => {
                const new_post = data.content;
                const old_post = document.getElementById(`p${post_id}`);
                old_post.innerHTML = new_post.replace(/\n/g, '<br>');
                modal.remove();
            })
        });
    })
}
let currentPage = 1;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function openModal(post_id) {
    const modal = document.createElement('div');
    modal.id = `modal${post_id}`;
    modal.className = 'modal';
    fetch(`/edit/${post_id}`, {method: 'GET' })
    .then(response => response.json())
    .then(data => {
        const post = data.post;
        let content = post.content;
        modal.innerHTML = `
            <div class="form-group">
                <textarea class="area" id="new-content" maxlength="150" rows = "7">${content}</textarea>
            </div>
            <button type="submit" id="edit-button" class="btn btn-primary">Edit</button>
        `;
        document.body.appendChild(modal);
        document.getElementById('edit-button').addEventListener('click', function(event) {
            event.preventDefault();
            const new_content = document.getElementById('new-content').value;
            fetch(`/edit/${post_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    content: new_content
                })
            })
            .then(response => response.json())
            .then(data => {
                const new_post = data.content;
                const old_post = document.getElementById(`p${post_id}`);
                old_post.innerHTML = new_post.replace(/\n/g, '<br>');
                modal.remove();
            })
        });
    })
}

let isRequestInProgress = false;

function manage_likes(post_id) {
    if (isRequestInProgress) {
        return;
    }
    isRequestInProgress = true;

    const csrfToken = getCookie('csrftoken');
    const heart = document.getElementById(`heart${post_id}`);
    let is_post_liked = heart.dataset.liked === 'true';

    if (is_post_liked)
        heart.classList.remove('fas', 'fa-heart', 'fa-1x');
    else
        heart.classList.remove('far', 'fa-heart', 'fa-1x');

    fetch(`/likes/${post_id}`, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
       },
        body: JSON.stringify({is_post_liked: is_post_liked}),
    })
    .then(response => response.json())
    .then(result => {
        const post_likes = result.likes;
        if (is_post_liked) {
            heart.style.color = 'grey';
            heart.classList.add('far', 'fa-heart', 'fa-1x');
        }
        else {
            heart.style.color = 'red';
            heart.classList.add('fas', 'fa-heart', 'fa-1x');
        }
        heart.textContent = `${post_likes} Likes`;
        heart.dataset.liked = !is_post_liked;
    })
    .finally(() => {
        isRequestInProgress = false;
    });
}