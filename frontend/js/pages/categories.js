const token = localStorage.getItem("token");
const user = JSON.parse(localStorage.getItem("user"));

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
    alert("AUTHORIZATION DENIED: Viewers cannot access raw category datasets.");
    window.location.href = "dashboard.html";
}

if (user.role === "ANALYST") {
    // Analysts can view Categories but cannot Define Structure
    const createSection = document.querySelector(".gs-table.p-4"); // Hides the card holding Define Structure
    if(createSection) createSection.style.display = "none";
    
    // Links to hide
    const userLink = document.getElementById("userLink");
    if(userLink) userLink.style.display = "none";
}


// 🔹 Load Categories
async function loadCategories() {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/categories?all=true`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();

        const table = document.getElementById("catTable");
        table.innerHTML = "";

        data.forEach(c => {
            // Visual indicators for active vs disabled
            const statusLabel = c.is_active 
                ? `<span class="badge border border-dark border-2 text-dark px-2 py-1 fs-6" style="background-color: var(--primary-color);">ACTIVE</span>` 
                : `<span class="badge border border-dark border-2 text-dark px-2 py-1 fs-6" style="background-color: var(--secondary-color);">DISABLED</span>`;
                
            const toggleButton = c.is_active
                ? `<button class="btn btn-neo py-1 px-3" style="background-color: var(--secondary-color);" onclick="toggleStatus(${c.id}, false)">Disable</button>`
                : `<button class="btn btn-neo py-1 px-3" style="background-color: var(--primary-color);" onclick="toggleStatus(${c.id}, true)">Enable</button>`;

            // Capitalize category name for presentation
            const presName = c.name.charAt(0).toUpperCase() + c.name.slice(1);

            // Action Buttons mapping (Hide for Analyst)
            const actionSection = user.role === "ADMIN" 
                ? ` <button class="btn btn-neo py-1 px-3 me-2 bg-white" onclick="openEditModal(${c.id}, '${c.name.replace(/'/g, "\\'")}')">Edit</button>
                    ${toggleButton}`
                : `<span class="fw-bold text-muted mt-2 d-inline-block">-- READ ONLY --</span>`;

            table.innerHTML += `
                <tr class="${!c.is_active ? 'opacity-75' : ''}">
                    <td class="text-dark align-middle">${c.id}</td>
                    <td class="text-dark fs-5 align-middle">${presName}</td>
                    <td class="text-dark align-middle">${statusLabel}</td>
                    <td class="text-center align-middle">
                        ${actionSection}
                    </td>
                </tr>
            `;
        });
    } catch(err) {
        console.error(err);
    }
    toggleLoader(false);
}

// 🔹 Create Category
async function createCategory() {
    const nameInput = document.getElementById("catName");
    const label = nameInput.value.trim();
    if (!label) return;

    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/categories`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ name: label })
        });
        
        const json = await res.json();
        if(!res.ok) alert(json.error || "Failed to create category");
        
        nameInput.value = "";
    } catch (err) {
        console.error(err);
    }
    await loadCategories();
}

// 🔹 Toggle Category Status
async function toggleStatus(id, newStatus) {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/categories/${id}/status`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ is_active: newStatus })
        });
        
        if(!res.ok) {
            const json = await res.json();
            alert(json.error || "Failed to toggle status");
        }
    } catch (err) {
        console.error(err);
    }
    await loadCategories();
}

// 🔹 Edit Modal Controller
let editModalInstance = null;

function openEditModal(id, currentName) {
    document.getElementById('editId').value = id;
    document.getElementById('editName').value = currentName;
    
    if(!editModalInstance) {
        editModalInstance = new bootstrap.Modal(document.getElementById('editModal'));
    }
    editModalInstance.show();
}

async function submitEdit() {
    const id = document.getElementById('editId').value;
    const newName = document.getElementById('editName').value.trim();
    
    if(!newName) return;

    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/categories/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ name: newName })
        });
        
        const json = await res.json();
        if(!res.ok) {
            alert(json.error || "Failed to edit category");
        } else {
            if(editModalInstance) editModalInstance.hide();
        }
    } catch (err) {
        console.error(err);
    }
    await loadCategories();
}

// 🔹 Logout
function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// 🔄 Initial Load
loadCategories();
