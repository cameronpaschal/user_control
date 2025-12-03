import {
  requireAuth,
  fetchJson,
  setStatus,
  decodeJwtPayload,
  wireLogoutButtons,
  setNavUser,
  getAccessToken,
} from "./api.js";

requireAuth();
setNavUser();
wireLogoutButtons();

const params = new URLSearchParams(window.location.search);
const userId = params.get("id");
const statusBox = document.querySelector("#user-status");
const content = document.querySelector("#user-content");
const genBtn = document.querySelector("#generate-email-link");
const resendBtn = document.querySelector("#resend-email-link");

if (!userId) {
  setStatus(statusBox, "Missing user id in query string", "error");
  throw new Error("Missing user id");
}

const payload = decodeJwtPayload(getAccessToken());
const isMe = payload?.user_id?.toString() === userId;

if (isMe) {
  genBtn.hidden = false;
  resendBtn.hidden = false;
}

function formatDate(date) {
  if (!date) return "—";
  const value = typeof date === "string" ? date : date.toString();
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleString();
}

async function loadUser() {
  setStatus(statusBox, "Loading user…", "info");
  try {
    const user = await fetchJson(`/users/${userId}`);
    renderUser(user);
    setStatus(statusBox, "", "info");
    statusBox.hidden = true;
  } catch (err) {
    setStatus(statusBox, err.message || "Unable to load user", "error");
  }
}

function renderUser(user) {
  content.innerHTML = `
    <div class="user-card">
      <div>
        <div class="eyebrow">Username</div>
        <div class="title">${user.username}</div>
        <div class="small">ID: ${user.user_id}</div>
      </div>
      <div>
        <div class="eyebrow">Display name</div>
        <div>${user.display_name || "—"}</div>
      </div>
      <div>
        <div class="eyebrow">Email</div>
        <div>${user.email}</div>
      </div>
      <div>
        <div class="eyebrow">Job title</div>
        <div>${user.job_title || "—"}</div>
      </div>
      <div>
        <div class="eyebrow">Email verified</div>
        <span class="pill ${user.email_verified_at ? "pill-success" : "pill-warn"}">
          ${user.email_verified_at ? "Verified" : "Unverified"}
        </span>
        <div class="small">${formatDate(user.email_verified_at)}</div>
      </div>
      <div>
        <div class="eyebrow">Created</div>
        <div>${formatDate(user.created_at)}</div>
      </div>
      <div>
        <div class="eyebrow">Updated</div>
        <div>${formatDate(user.updated_at)}</div>
      </div>
      <div>
        <div class="eyebrow">Bio</div>
        <div>${user.bio || "—"}</div>
      </div>
    </div>
  `;
}

async function requestEmailLink(endpoint) {
  setStatus(statusBox, "Working…", "info");
  try {
    const data = await fetchJson(endpoint, { method: "POST" });
    setStatus(statusBox, `Verification link: ${data.url}`, "success");
  } catch (err) {
    setStatus(statusBox, err.message || "Unable to request link", "error");
  }
}

genBtn?.addEventListener("click", () => requestEmailLink("/auth/gen-email-verify"));
resendBtn?.addEventListener("click", () => requestEmailLink("/auth/resend-email-verify"));

loadUser();
