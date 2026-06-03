const API_URL = 'http://localhost:8000';

async function loadProjects() {
    try {
        const res = await fetch(`${API_URL}/projects/`);
        const projects = await res.json();
        const container = document.getElementById('projects-list');

        if (projects.length === 0) {
            container.innerHTML = '<p class="text-gray-500">Проектов пока нет. Добавьте первый!</p>';
            return;
        }

        container.innerHTML = projects.map(p => `
            <div class="bg-white p-4 rounded shadow flex justify-between items-center border-l-4 border-blue-500">
                <div>
                    <h3 class="font-bold text-lg text-gray-800">${p.name}</h3>
                    <p class="text-sm text-gray-600">${p.city}, ${p.address || 'Адрес не указан'}</p>
                    <p class="text-xs text-gray-500 mt-1">Вознаграждение: <span class="font-semibold text-green-600">${p.reward_percent}%</span></p>
                </div>
                <button onclick="deleteProject(${p.id})" class="text-red-500 hover:text-red-700 text-sm font-medium">Удалить</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка загрузки проектов:', error);
    }
}

document.getElementById('add-project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    if (data.price_from) data.price_from = parseFloat(data.price_from);
    if (data.reward_percent) data.reward_percent = parseFloat(data.reward_percent);

    await fetch(`${API_URL}/projects/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    e.target.reset();
    loadProjects();
});

async function deleteProject(id) {
    if (confirm('Удалить проект?')) {
        await fetch(`${API_URL}/projects/${id}`, { method: 'DELETE' });
        loadProjects();
    }
}

async function loadKB() {
    try {
        const res = await fetch(`${API_URL}/knowledge/`);
        const items = await res.json();
        const container = document.getElementById('kb-list');

        if (items.length === 0) {
            container.innerHTML = '<p class="text-gray-500">База знаний пуста.</p>';
            return;
        }

        container.innerHTML = items.map(k => `
            <div class="bg-white p-4 rounded shadow border-l-4 border-green-500">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-1">
                            <h4 class="font-semibold text-gray-800">${k.question}</h4>
                            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">${k.category || 'Общее'}</span>
                        </div>
                        <p class="text-sm text-gray-700">${k.answer}</p>
                    </div>
                    <button onclick="deleteKB(${k.id})" class="text-red-500 hover:text-red-700 ml-4">Удалить</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка загрузки БЗ:', error);
    }
}

document.getElementById('add-kb-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    if (data.project_id) data.project_id = parseInt(data.project_id);

    await fetch(`${API_URL}/knowledge/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    e.target.reset();
    loadKB();
});

async function deleteKB(id) {
    if (confirm('Удалить запись из базы знаний?')) {
        await fetch(`${API_URL}/knowledge/${id}`, { method: 'DELETE' });
        loadKB();
    }
}

async function loadRewards() {
    try {
        const res = await fetch(`${API_URL}/rewards/`);
        const items = await res.json();
        const container = document.getElementById('rewards-list');

        if (items.length === 0) {
            container.innerHTML = '<p class="text-gray-500">Вознаграждений пока нет.</p>';
            return;
        }

        container.innerHTML = items.map(r => `
            <div class="bg-white p-4 rounded shadow flex justify-between items-center border-l-4 border-purple-500">
                <div>
                    <span class="font-bold text-2xl text-purple-600">${r.reward_percent}%</span>
                    <span class="text-gray-600 ml-2 text-sm">для проекта ID: ${r.project_id}</span>
                    <p class="text-sm text-gray-500 mt-1">${r.description || 'Нет описания'}</p>
                </div>
                <button onclick="deleteReward(${r.id})" class="text-red-500 hover:text-red-700 text-sm">Удалить</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Ошибка загрузки вознаграждений:', error);
    }
}

document.getElementById('add-reward-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    if (data.project_id) data.project_id = parseInt(data.project_id);
    if (data.reward_percent) data.reward_percent = parseFloat(data.reward_percent);

    await fetch(`${API_URL}/rewards/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    e.target.reset();
    loadRewards();
});

async function deleteReward(id) {
    if (confirm('Удалить вознаграждение?')) {
        await fetch(`${API_URL}/rewards/${id}`, { method: 'DELETE' });
        loadRewards();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    loadKB();
    loadRewards();
});