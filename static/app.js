const API = 'http://127.0.0.1:8000';
let currentProblemId = null;

// ── Page Navigation ──────────────────────────────

function showPage(page) {
    const pages = ['problems', 'problem-detail', 'login', 'register', 'submissions'];
    pages.forEach(p => {
        document.getElementById(`page-${p}`).style.display = 'none';
    });
    document.getElementById(`page-${page}`).style.display = page === 'problem-detail' ? 'grid' : 'block';

    if (page === 'problems')     loadProblems();
    if (page === 'submissions')  loadSubmissions();
}

// ── Auth ─────────────────────────────────────────

function getToken()  { return localStorage.getItem('token'); }
function isLoggedIn(){ return !!getToken(); }

function updateNavbar() {
    const username = localStorage.getItem('username');
    if (isLoggedIn()) {
        document.getElementById('nav-auth').style.display = 'none';
        document.getElementById('nav-user').style.display = 'inline-flex';
        document.getElementById('nav-username').textContent = username;
    } else {
        document.getElementById('nav-auth').style.display = 'inline-flex';
        document.getElementById('nav-user').style.display = 'none';
    }
}

async function login() {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    document.getElementById('login-error').textContent = '';

    const res = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', username);
        updateNavbar();
        showPage('problems');
    } else {
        document.getElementById('login-error').textContent = 'Invalid username or password.';
    }
}

async function register() {
    const username = document.getElementById('register-username').value.trim();
    const email    = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;
    document.getElementById('register-error').textContent = '';

    const res = await fetch(`${API}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });

    if (res.ok) {
        showPage('login');
    } else {
        const data = await res.json();
        document.getElementById('register-error').textContent = data.detail || 'Registration failed.';
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    updateNavbar();
    showPage('problems');
}

// ── Problems ─────────────────────────────────────

async function loadProblems() {
    const res = await fetch(`${API}/problems/`);
    const problems = await res.json();
    const tbody = document.getElementById('problems-list');
    tbody.innerHTML = '';

    problems.forEach((p, i) => {
        tbody.innerHTML += `
            <tr onclick="openProblem(${p.id})">
                <td>${i + 1}</td>
                <td><span class="problem-title-link">${p.title}</span></td>
                <td><span class="badge ${p.difficulty}">${p.difficulty}</span></td>
                <td>${p.time_limit}s</td>
            </tr>
        `;
    });
}

async function openProblem(id) {
    const res = await fetch(`${API}/problems/${id}`);
    const problem = await res.json();
    currentProblemId = id;

    document.getElementById('problem-title').textContent       = problem.title;
    document.getElementById('problem-difficulty').textContent  = problem.difficulty;
    document.getElementById('problem-difficulty').className    = `badge ${problem.difficulty}`;
    document.getElementById('problem-timelimit').textContent   = `⏱ ${problem.time_limit}s`;
    document.getElementById('problem-description').textContent = problem.description;
    document.getElementById('code-editor').value               = '';
    document.getElementById('verdict-box').style.display       = 'none';

    showPage('problem-detail');
}

// ── Submit ────────────────────────────────────────

async function submitCode() {
    if (!isLoggedIn()) { showPage('login'); return; }

    const code = document.getElementById('code-editor').value;
    if (!code.trim()) return;

    const verdictBox     = document.getElementById('verdict-box');
    const verdictText    = document.getElementById('verdict-text');
    const verdictRuntime = document.getElementById('verdict-runtime');

    verdictBox.style.display    = 'block';
    verdictText.className       = 'verdict-text verdict-judging';
    verdictText.innerHTML = '<span class="spinner"></span> Judging...';
    verdictRuntime.textContent  = '';

    try {
        const res = await fetch(`${API}/submissions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({ problem_id: currentProblemId, code })
        });

        const data = await res.json();
        verdictText.textContent = data.verdict;
        verdictText.className   = `verdict-text verdict-${data.verdict}`;
        verdictRuntime.textContent = `Runtime: ${data.runtime} ms`;
    } catch {
        verdictText.textContent = 'Error';
        verdictText.className   = 'verdict-text verdict-RE';
    }
}

// ── Submissions ───────────────────────────────────

async function loadSubmissions() {
    if (!isLoggedIn()) { showPage('login'); return; }

    const list = document.getElementById('submissions-list');
    list.innerHTML = '<p class="empty-state">Loading...</p>';

    const res = await fetch(`${API}/submissions/me/all`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });

    const submissions = await res.json();

    if (!submissions.length) {
        list.innerHTML = '<div class="empty-state">📭<p>No submissions yet. Pick a problem and start solving!</p></div>';
        return;
    }

    list.innerHTML = `
        <table class="submissions-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Problem</th>
                    <th>Verdict</th>
                    <th>Runtime</th>
                    <th>Submitted At</th>
                </tr>
            </thead>
            <tbody>
                ${submissions.map(s => `
                    <tr>
                        <td>${s.id}</td>
                        <td>${s.problem_id}</td>
                        <td><span class="verdict-text verdict-${s.verdict}" style="font-size:13px">${s.verdict}</span></td>
                        <td>${s.runtime} ms</td>
                        <td>${new Date(s.submitted_at).toLocaleString()}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// ── Init ──────────────────────────────────────────

updateNavbar();
showPage('problems');