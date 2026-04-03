const token = localStorage.getItem("token");
const user = JSON.parse(localStorage.getItem("user"));

let showDeleted = false;
let currentPage = 1;
let currentPerPage = 10;
let totalPages = 1;

if (!token) {
    window.location.href = "login.html";
}

// 🌐 Global Loader Toggle
function toggleLoader(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        if (show) loader.classList.remove('d-none');
        else loader.classList.add('d-none');
    }
}

// 🔐 Role-based UI & RBAC
if (user.role === "VIEWER") {
    alert("AUTHORIZATION DENIED: Viewers cannot access raw transaction ledgers.");
    window.location.href = "dashboard.html";
}

if (user.role === "ANALYST") {
    // Analysts can view, but cannot create or manipulate data blocks
    const adminSection = document.getElementById("adminSection");
    if(adminSection) adminSection.style.display = "none";
    
    // Disable access to Recycle Bin for Analysts
    const recycleBtn = document.getElementById("toggleRecycleBtn");
    if(recycleBtn) recycleBtn.style.display = "none";
    
    const userLink = document.getElementById("userLink");
    if(userLink) userLink.style.display = "none";
}

// 🔹 Load Categories
async function loadCategories() {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/categories`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();
        
        const dropdown = document.getElementById("category");
        const editDropdown = document.getElementById("editCategory");
        const filterDropdown = document.getElementById("filterCategory");

        if(dropdown) dropdown.innerHTML = "";
        if(editDropdown) editDropdown.innerHTML = "";
        if(filterDropdown) filterDropdown.innerHTML = '<option value="">All Categories</option>';

        data.forEach(c => {
            if(dropdown) dropdown.innerHTML += `<option value="${c.id}">${c.name}</option>`;
            if(editDropdown) editDropdown.innerHTML += `<option value="${c.id}">${c.name}</option>`;
            if(filterDropdown) filterDropdown.innerHTML += `<option value="${c.id}">${c.name}</option>`;
        });
    } catch(err) {
        console.error(err);
    }
    toggleLoader(false);
}

// 🔹 Load Transactions (With Filters)
async function loadTransactions() {
    toggleLoader(true);
    let url = `${CONFIG.API_BASE_URL}/transactions?page=${currentPage}&per_page=${currentPerPage}`;
    if (showDeleted) url += "&deleted=true";

    // Grab filters
    const fSearch = document.getElementById("filterSearch")?.value.trim();
    const fType = document.getElementById("filterType")?.value;
    const fCat = document.getElementById("filterCategory")?.value;
    const fDate = document.getElementById("filterDate")?.value;
    const fSort = document.getElementById("filterSort")?.value;

    if (fSearch) url += `&search=${encodeURIComponent(fSearch)}`;
    if (fType) url += `&type=${fType}`;
    if (fCat) url += `&category_id=${fCat}`;
    if (fDate) url += `&date=${fDate}`;
    if (fSort) url += `&sort_by=${fSort}`;

    try {
        const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
        const data = await res.json();

        const table = document.getElementById("txnTable");
        table.innerHTML = "";

        // Check if backend returns paginated object API
        const items = data.transactions || data; 
        
        if (data.total !== undefined) {
            totalPages = data.pages;
            document.getElementById("pageInfo").innerText = `Page ${data.page} / ${data.pages}`;
        }

        items.forEach(t => {
            const rowDataStr = encodeURIComponent(JSON.stringify(t));
            table.innerHTML += `
                <tr>
                    <td class="text-dark">${t.id}</td>
                    <td class="text-dark">${t.amount}</td>
                    <td class="text-dark">${t.type}</td>
                    <td class="text-dark">${t.category}</td>
                    <td class="text-dark">${t.date}</td>
                    <td class="text-dark">${t.description || ""}</td>
                    <td class="text-dark">${t.created_by}</td>
                    <td class="text-center">${user.role === "ADMIN" ? actionButtons(t, rowDataStr) : ""}</td>
                </tr>
            `;
        });
    } catch(err) {
        console.error(err);
    }
    toggleLoader(false);
}

// 🔹 Action Buttons
function actionButtons(t, rowStr) {
    if (showDeleted) {
        return `
            <button class="btn btn-neo py-1 px-2 mb-1" style="background-color: var(--secondary-color);" onclick="permanentDelete(${t.id})">Delete Forev</button>
            <button class="btn btn-neo py-1 px-2 mb-1" style="background-color: var(--primary-color);" onclick="restoreTransaction(${t.id})">Restore Data</button>
        `;
    }

    return `
        <button class="btn btn-neo py-1 px-3 me-1 bg-white" onclick="openEditModal('${rowStr}')">Edit</button>
        <button class="btn btn-neo py-1 px-3" style="background-color: var(--secondary-color);" onclick="deleteTransaction(${t.id})">Bin</button>
    `;
}

// 🔹 Pagination Handlers
function changePage(direction) {
    if (direction === -1 && currentPage > 1) {
        currentPage--;
        loadTransactions();
    } else if (direction === 1 && currentPage < totalPages) {
        currentPage++;
        loadTransactions();
    }
}

function changePerPage() {
    const val = document.getElementById('perPage').value;
    currentPerPage = parseInt(val);
    currentPage = 1;
    loadTransactions();
}

// 🔹 Filter Subsystems
function applyFilters() {
    currentPage = 1;
    loadTransactions();
}

function resetFilters() {
    document.getElementById("filterSearch").value = "";
    document.getElementById("filterType").value = "";
    document.getElementById("filterCategory").value = "";
    document.getElementById("filterDate").value = "";
    document.getElementById("filterSort").value = "created_desc";
    currentPage = 1;
    loadTransactions();
}

// 🔹 Create Transaction
async function createTransaction() {
    toggleLoader(true);
    const body = {
        amount: document.getElementById("amount").value,
        type: document.getElementById("type").value,
        category_id: document.getElementById("category").value,
        date: document.getElementById("date").value,
        description: document.getElementById("desc").value
    };

    await fetch(`${CONFIG.API_BASE_URL}/transactions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
    });

    await loadTransactions();
}

// 🔹 Soft Delete
async function deleteTransaction(id) {
    toggleLoader(true);
    await fetch(`${CONFIG.API_BASE_URL}/transactions/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
    });
    await loadTransactions();
}

// 🔹 Restore Transaction
async function restoreTransaction(id) {
    toggleLoader(true);
    await fetch(`${CONFIG.API_BASE_URL}/transactions/${id}/restore`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${token}` }
    });
    await loadTransactions();
}

// 🔹 Permanent Delete
async function permanentDelete(id) {
    if(!confirm("Are you sure you want to completely erase this record?")) return;
    toggleLoader(true);
    await fetch(`${CONFIG.API_BASE_URL}/transactions/${id}/permanent`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
    });
    await loadTransactions();
}

// 🔹 Toggle Recycle Bin
function toggleRecycle() {
    showDeleted = !showDeleted;
    currentPage = 1; // Reset to page 1 on toggle
    loadTransactions();
}

// 🔹 Edit Modal Subsystems
let editModalInstance = null;

function openEditModal(rowStr) {
    const t = JSON.parse(decodeURIComponent(rowStr));
    
    document.getElementById('editId').value = t.id;
    document.getElementById('editAmount').value = t.amount;
    document.getElementById('editType').value = t.type;
    
    const catSelect = document.getElementById('editCategory');
    for (let i = 0; i < catSelect.options.length; i++) {
        if (catSelect.options[i].text === t.category) {
            catSelect.selectedIndex = i;
            break;
        }
    }
    
    document.getElementById('editDate').value = t.date;
    document.getElementById('editDesc').value = t.description;
    
    if(!editModalInstance) {
        editModalInstance = new bootstrap.Modal(document.getElementById('editModal'));
    }
    editModalInstance.show();
}

async function submitEdit() {
    const id = document.getElementById('editId').value;
    const body = {
        amount: document.getElementById("editAmount").value,
        type: document.getElementById("editType").value,
        category_id: document.getElementById("editCategory").value,
        date: document.getElementById("editDate").value,
        description: document.getElementById("editDesc").value
    };

    toggleLoader(true);
    await fetch(`${CONFIG.API_BASE_URL}/transactions/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
    });
    
    if(editModalInstance) editModalInstance.hide();
    await loadTransactions();
}

// 🔹 Logout
function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// 🔄 Initial Trigger
loadCategories();
loadTransactions();