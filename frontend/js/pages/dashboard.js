const token = localStorage.getItem("token");

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

async function loadDashboard() {
    toggleLoader(true);
    try {
        const res = await fetch(`${CONFIG.API_BASE_URL}/dashboard/summary`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

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