import { requireAuth, fetchJson, setStatus, wireLogoutButtons, setNavUser } from "./api.js";

requireAuth();
setNavUser();
wireLogoutButtons();

const tbody = document.querySelector("#users-body");
const statusBox = document.querySelector("#users-status");
const refreshBtn = document.querySelector("#refresh-users");

async function loadUsers() {
  setStatus(statusBox, "Loading users…", "info");
  tbody.innerHTML = "";
  try {
    const users = await fetchJson("/users");
    if (!users.length) {
      tbody.innerHTML = `<tr><td colspan="6" class="muted">No users found</td></tr>`;
      setStatus(statusBox, "", "info");
      statusBox.hidden = true;
      return;
    }
    for (const user of users) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${user.user_id}</td>
        <td>${user.username}</td>
        <td>${user.email}</td>
        <td>${user.job_title || "—"}</td>
        <td>${user.email_verified_at ? '<span class="pill pill-success">Verified</span>' : '<span class="pill pill-warn">Unverified</span>'}</td>
        <td><a href="./user.html?id=${user.user_id}">View</a></td>
      `;
      tbody.appendChild(row);
    }
    setStatus(statusBox, "", "info");
    statusBox.hidden = true;
  } catch (err) {
    setStatus(statusBox, err.message || "Unable to load users", "error");
  }
}

refreshBtn?.addEventListener("click", loadUsers);
loadUsers();
