import {
  requireAuth,
  fetchJson,
  setStatus,
  decodeJwtPayload,
  getAccessToken,
  wireLogoutButtons,
  setNavUser,
} from "./api.js";

requireAuth();
setNavUser();
wireLogoutButtons();

const tokenPreview = document.querySelector("#token-preview");
const currentUserEl = document.querySelector("#current-user");
const statusBox = document.querySelector("#dashboard-status");
const generateLinkBtn = document.querySelector("#generate-link");

function updateTokenPreview() {
  const token = getAccessToken();
  if (!token) {
    tokenPreview.textContent = "No access token found. Sign in again.";
    return;
  }
  const payload = decodeJwtPayload(token);
  const short = `${token.slice(0, 16)}…${token.slice(-12)}`;
  tokenPreview.textContent = `${short} (exp: ${payload?.exp ? new Date(payload.exp * 1000).toLocaleString() : "unknown"})`;
}

async function loadCurrentUser() {
  const payload = decodeJwtPayload(getAccessToken());
  if (!payload?.user_id) {
    currentUserEl.textContent = "No current user loaded yet.";
    return;
  }
  try {
    const me = await fetchJson(`/users/${payload.user_id}`);
    currentUserEl.innerHTML = `
      <div class="user-card">
        <div>
          <div class="eyebrow">Username</div>
          <div>${me.username}</div>
        </div>
        <div>
          <div class="eyebrow">Email</div>
          <div>${me.email}</div>
        </div>
        <div>
          <div class="eyebrow">Display name</div>
          <div>${me.display_name || "—"}</div>
        </div>
        <div>
          <div class="eyebrow">Status</div>
          <span class="pill ${me.email_verified_at ? "pill-success" : "pill-warn"}">${me.email_verified_at ? "Verified" : "Unverified"}</span>
        </div>
      </div>
    `;
  } catch (err) {
    currentUserEl.textContent = err.message || "Unable to load user.";
  }
}

generateLinkBtn?.addEventListener("click", async () => {
  setStatus(statusBox, "Requesting verification link…", "info");
  try {
    const data = await fetchJson("/auth/gen-email-verify", { method: "POST" });
    setStatus(statusBox, `Verification link generated: ${data.url}`, "success");
  } catch (err) {
    setStatus(statusBox, err.message || "Could not generate link", "error");
  }
});

updateTokenPreview();
loadCurrentUser();
