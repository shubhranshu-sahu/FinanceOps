const token = localStorage.getItem("token");
const user = JSON.parse(localStorage.getItem("user") || "null");

if (!token || !user) {
    window.location.href = "login.html";
}

// 🔐 Role-based check for Nav Bar visual hygiene
if (user.role === "VIEWER") {
    const txnL = document.getElementById("txnLink");
    const catL = document.getElementById("catLink");
    const userL = document.getElementById("userLink");
    if (txnL) txnL.style.display = "none";
    if (catL) catL.style.display = "none";
    if (userL) userL.style.display = "none";
} else if (user.role === "ANALYST") {
    const userL = document.getElementById("userLink");
    if (userL) userL.style.display = "none";
}

//  Global Loader Toggle
function toggleLoader(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        if (show) loader.classList.remove('d-none');
        else loader.classList.add('d-none');
    }
}

async function loadDashboard() {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/dashboard/summary`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (res.status === 401 || res.status === 403) {
            alert("SECURITY EXCEPTION: Unauthorized access or tampered session detected.");
            localStorage.clear();
            window.location.href = "login.html";
            return;
        }

        const data = await res.json();

        document.getElementById("income").innerText = data.total_income;
        document.getElementById("expense").innerText = data.total_expense;
        document.getElementById("balance").innerText = data.net_balance;

        // Recent Transactions
        const table = document.getElementById("recentTable");
        table.innerHTML = "";

        data.recent_transactions.forEach(txn => {
            const row = `
                <tr>
                    <td class="text-dark">${txn.id}</td>
                    <td class="text-dark">${txn.amount}</td>
                    <td class="text-dark">${txn.type}</td>
                    <td class="text-dark">${txn.category}</td>
                    <td class="text-dark">${txn.date}</td>
                </tr>
            `;
            table.innerHTML += row;
        });


        // Category Breakdown
        const catTable = document.getElementById("categoryTable");
        catTable.innerHTML = "";

        data.category_breakdown.forEach(c => {
            catTable.innerHTML += `
        <tr>
            <td class="text-dark">${c.category}</td>
            <td class="text-dark">${c.total}</td>
        </tr>
    `;
        });


        // Monthly Trends
        const trendTable = document.getElementById("trendTable");
        trendTable.innerHTML = "";

        data.monthly_trends.forEach(t => {
            trendTable.innerHTML += `
            <tr>
                <td class="text-dark">${t.month}</td>
                <td class="text-dark">${t.total}</td>
            </tr>
        `;
        });

    } catch (err) {
        console.error(err);
        alert("Failed to load dashboard");
    }

    toggleLoader(false);
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

loadDashboard();