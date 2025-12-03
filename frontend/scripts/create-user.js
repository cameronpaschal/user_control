import { requireAuth, fetchJson, setStatus, wireLogoutButtons, setNavUser } from "./api.js";

requireAuth();
setNavUser();
wireLogoutButtons();

const form = document.querySelector("#create-form");
const statusBox = document.querySelector("#create-status");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const payload = {
    username: data.get("username")?.toString().trim(),
    display_name: data.get("display_name")?.toString().trim(),
    email: data.get("email")?.toString().trim(),
    job_title: data.get("job_title")?.toString().trim(),
    password: data.get("password")?.toString(),
    bio: data.get("bio")?.toString().trim() || null,
  };

  setStatus(statusBox, "Creating user…", "info");
  try {
    const res = await fetchJson("/users/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const newId = res?.user_id;
    setStatus(statusBox, `User created with id ${newId}`, "success");
    if (newId) {
      setTimeout(() => {
        window.location.href = `./user.html?id=${newId}`;
      }, 400);
    }
  } catch (err) {
    setStatus(statusBox, err.message || "Unable to create user", "error");
  }
});
