document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const errorDiv = document.getElementById("error");
    const successDiv = document.getElementById("success");

    const btn = document.querySelector("button[type='submit']");
    const originalText = btn.innerText;

    errorDiv.innerText = "";
    successDiv.innerText = "";
    btn.innerText = "Registering...";
    btn.disabled = true;

    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Registration failed");
        }

        successDiv.innerText = "Registration successful! Redirecting to login...";

        // Redirect after short delay
        setTimeout(() => {
            window.location.href = "login.html";
        }, 1500);

    } catch (error) {
        errorDiv.innerText = error.message;
    } finally {
        if (!successDiv.innerText) {
            btn.innerText = originalText;
            btn.disabled = false;
        }
    }
});