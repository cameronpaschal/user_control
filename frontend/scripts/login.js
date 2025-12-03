import { fetchJson, setAccessToken, setStatus } from "./api.js";

const form = document.querySelector("#login-form");
const statusBox = document.querySelector("#login-status");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const username = formData.get("username")?.toString().trim();
  const password = formData.get("password")?.toString();

  if (!username || !password) {
    setStatus(statusBox, "Username and password are required", "error");
    return;
  }

  setStatus(statusBox, "Signing in…", "info");

  try {
    const data = await fetchJson("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (data?.access_token) {
      setAccessToken(data.access_token);
    }
    setStatus(statusBox, "Signed in! Redirecting…", "success");
    setTimeout(() => {
      window.location.href = "./dashboard.html";
    }, 400);
  } catch (err) {
    setStatus(statusBox, err.message || "Unable to sign in", "error");
  }
});
