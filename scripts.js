document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.querySelector("#signup form");
    const loginForm = document.querySelector("#login form");

    signupForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(signupForm);
        const data = {
            username: formData.get("username"),
            email: formData.get("email"),
            password: formData.get("password"),
        };

        try {
            const response = await fetch("/users/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });
            if (response.ok) {
                alert("User created successfully!");
            } else {
                const result = await response.json();
                alert(`Error: ${result.detail}`);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while creating the user.");
        }
    });

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const data = new URLSearchParams();
        data.append("username", formData.get("username"));
        data.append("password", formData.get("password"));

        try {
            const response = await fetch("/token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: data,
            });
            if (response.ok) {
                const result = await response.json();
                localStorage.setItem("token", result.access_token);
                alert("Login successful!");
                fetchRecommendations();
            } else {
                const result = await response.json();
                alert(`Error: ${result.detail}`);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while logging in.");
        }
    });

    async function fetchRecommendations() {
        const token = localStorage.getItem("token");
        if (!token) return;

        try {
            const response = await fetch("/recommendations/1/", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const songs = await response.json();
                const songList = document.getElementById("song-list");
                songList.innerHTML = "";
                songs.forEach(song => {
                    const li = document.createElement("li");
                    li.textContent = song.title;
                    songList.appendChild(li);
                });
            } else {
                alert("Failed to fetch recommendations.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while fetching recommendations.");
        }
    }
});

