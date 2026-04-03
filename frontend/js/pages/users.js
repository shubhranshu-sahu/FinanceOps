const token = localStorage.getItem("token");
const user = JSON.parse(localStorage.getItem("user"));

if (!token) {
    window.location.href = "login.html";
}

//  Global Loader Toggle
function toggleLoader(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        if (show) loader.classList.remove('d-none');
        else loader.classList.add('d-none');
    }
}

// 🔐 Role-based check (Only ADMINS should be in this section)
if (user.role !== "ADMIN") {
    alert("Unauthorized Phase Check. Admin privileges required.");
    window.location.href = "dashboard.html";
}


// 🔹 Load Users Ledger
async function loadUsers() {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/users`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();

        const table = document.getElementById("userTable");
        table.innerHTML = "";

        data.forEach(u => {
            // Visual indicators for access vs frozen
            const statusLabel = u.is_active
                ? `<span class="badge border border-dark border-2 text-dark px-2 py-1 fs-6" style="background-color: var(--primary-color);">CLEARED</span>`
                : `<span class="badge border border-dark border-2 text-dark px-2 py-1 fs-6" style="background-color: var(--secondary-color);">FROZEN</span>`;

            // Visual indicator for role level
            let roleStyle = "background-color: #e5e7eb;"; // Default gray for viewer
            if (u.role === "ADMIN") roleStyle = "background-color: #fca5a5;"; // Red for Admin
            if (u.role === "ANALYST") roleStyle = "background-color: #fde047;"; // Yellow for Analyst
            const roleLabel = `<span class="badge border border-dark border-2 text-dark px-2 py-1 fs-6" style="${roleStyle}">${u.role}</span>`;

            // Self-lock safeguard (Never let user disable themselves)
            const isSelf = u.id === user.id;

            const toggleButton = u.is_active
                ? `<button class="btn btn-neo py-1 px-3 ${isSelf ? "d-none" : ""}" style="background-color: var(--secondary-color);" onclick="toggleFreeze(${u.id}, false)">Freeze</button>`
                : `<button class="btn btn-neo py-1 px-3 ${isSelf ? "d-none" : ""}" style="background-color: var(--primary-color);" onclick="toggleFreeze(${u.id}, true)">Unfreeze</button>`;

            const editBtn = `<button class="btn btn-neo py-1 px-3 me-2 bg-white ${isSelf ? "d-none" : ""}" onclick="openRoleModal(${u.id}, '${u.name.replace(/'/g, "\\'")}', '${u.role}')">Modify</button>`;

            table.innerHTML += `
                <tr class="${!u.is_active ? 'opacity-75 bg-light' : ''}">
                    <td class="text-dark fs-5 align-middle">${u.id}</td>
                    <td class="text-dark fs-5 align-middle">${u.name}</td>
                    <td class="text-dark fs-6 font-monospace align-middle">${u.email}</td>
                    <td class="text-dark align-middle">${roleLabel}</td>
                    <td class="text-dark align-middle">${statusLabel}</td>
                    <td class="text-center align-middle">
                        ${isSelf ? '<span class="fw-bold text-muted mt-2 d-inline-block">-- CORE IDENTITY --</span>' : editBtn + toggleButton}
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
    }
    toggleLoader(false);
}

// 🔹 Toggle Freeze Status (Enable/Disable)
async function toggleFreeze(id, newStatus) {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/users/${id}/status`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ is_active: newStatus })
        });

        if (!res.ok) {
            const json = await res.json();
            alert(json.error || "Failed to alter status node");
        }
    } catch (err) {
        console.error(err);
    }
    await loadUsers();
}

// 🔹 Modal Controllers
let roleModalInstance = null;

function openRoleModal(id, currentName, currentRole) {
    document.getElementById('editUserId').value = id;
    document.getElementById('editUserName').innerText = currentName.toUpperCase();
    document.getElementById('editRole').value = currentRole;

    if (!roleModalInstance) {
        roleModalInstance = new bootstrap.Modal(document.getElementById('roleModal'));
    }
    roleModalInstance.show();
}

// 🔹 Escalate / Modify Role
async function submitRoleUpdate() {
    const id = document.getElementById('editUserId').value;
    const newRole = document.getElementById('editRole').value;

    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/users/${id}/role`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ role: newRole })
        });

        if (!res.ok) {
            const json = await res.json();
            alert(json.error || "Failed to modify role");
        } else {
            if (roleModalInstance) roleModalInstance.hide();
        }
    } catch (err) {
        console.error(err);
    }
    await loadUsers();
}

// 🔹 Logout Function
function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// 🔄 Initiator
loadUsers();
