if (!localStorage.getItem('token')) {
    alert('Please login first.');
    window.location.href = 'login.html';
}

async function fetchThreads() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/forum', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const threaddiv = document.getElementById('threads');
        threaddiv.innerHTML='';

        response.data.forEach(thread => {
            const div = document.createElement('div');
            div.className = 'forum-container';
            div.innerHTML = `
                <h5>${thread.title}</h5>
                <p>${thread.content}</p>
                <div id="commments-${thread.threadID}"></div>
                <div class="mt-3">
                    <input type="text" id="comment-${thread.threadID}" class="form-control mb-2" placeholder="Write a comment ">
                    <button class="btn btn-primary btn-sm" onclick="postComment(${thread.threadID})">Post</button>
                </div>
            `;
            threaddiv.appendChild(div);
            fetchComments(thread.threadID);
        });
    }
    catch (error) {
        console.error(error)
        alert('Failed to load forum threads.');
    }
}

document.getElementById('threadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value.trim();
    const content = document.getElementById('content').value.trim();

    try {
        await axios.post('http://127.0.0.1:8000/forum', { title, content }, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert('Thread posted!');
        document.getElementById('threadForm').reset();
        fetchThreads();
    }
    catch (error) {
        console.error(error)
        alert('Failed to post thread.');
    }

});

async function postComment(threadID) {
    const comContent = document.getElementById('`comment-${threadID').value.trim();
    if (!comContent) return;

    try {
        await axios.post(`http://127.0.0.1:8000/forum/${threadID}/comment`, {content:comContent}, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert('Comment posted');
        fetchThreads();
    }
    catch (error) {
        console.error(error);
        alert('Failed to post comment');
    }
}

async function fetchComments(threadID) {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/forum/${threadID}/comment`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const commentdiv = document.getElementById('comments-${threadID}');
        commentdiv.innerHTML = '';

        response.data.forEach(assign => {
            const div = document.createElement('div');
            div.className = 'comment-container';
            div.innerHTML = `<small>Due: ${new Date(assign.dueDate).toLocaleDateString()}</small>`;
            commentdiv.appendChild(div);
        });
    }
    catch (error) {
        console.error(error);
    }
}

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
});

fetchThreads();
