const API_BASE = window.API_BASE || localStorage.getItem("API_BASE") || "http://localhost:8000";
const ACCESS_TOKEN_KEY = "uc_access_token";

export function setAccessToken(token) {
  localStorage.setItem(ACCESS_TOKEN_KEY, token);
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function clearAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
}

export function decodeJwtPayload(token) {
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length < 2) return null;
  try {
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const json = atob(base64);
    return JSON.parse(json);
  } catch (err) {
    console.warn("Failed to decode token", err);
    return null;
  }
}

async function refreshToken() {
  try {
    const res = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });
    if (!res.ok) return null;
    const data = await res.json();
    if (data?.access_token) {
      setAccessToken(data.access_token);
      return data.access_token;
    }
  } catch (err) {
    console.error("Refresh failed", err);
  }
  return null;
}

export async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = getAccessToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const opts = {
    ...options,
    headers,
    credentials: options.credentials ?? "include",
  };

  let res = await fetch(`${API_BASE}${path}`, opts);

  if (res.status === 401) {
    const newToken = await refreshToken();
    if (newToken) {
      headers.set("Authorization", `Bearer ${newToken}`);
      res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
    } else {
      clearAccessToken();
    }
  }

  return res;
}

export async function fetchJson(path, options = {}) {
  const res = await apiFetch(path, options);
  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    data = null;
  }
  if (!res.ok) {
    const message = data?.detail || data?.status || data?.error || "Request failed";
    throw new Error(message);
  }
  return data;
}

export function requireAuth() {
  if (!getAccessToken()) {
    window.location.href = "./index.html";
  }
}

export function logout() {
  clearAccessToken();
  window.location.href = "./index.html";
}

export function setStatus(el, message, type = "info") {
  if (!el) return;
  el.textContent = message;
  el.dataset.type = type;
  el.hidden = !message;
}

export function renderUserSummary(target, user) {
  if (!target || !user) return;
  const verified = user.email_verified_at ? "Verified" : "Unverified";
  target.innerHTML = `
    <div class="user-card">
      <div>
        <div class="eyebrow">Username</div>
        <div class="title">${user.username}</div>
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
        <div class="eyebrow">Status</div>
        <span class="pill ${user.email_verified_at ? "pill-success" : "pill-warn"}">${verified}</span>
      </div>
    </div>
  `;
}

export function wireLogoutButtons() {
  document.querySelectorAll("[data-action='logout']").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  });
}

export function setNavUser() {
  const slot = document.querySelector("[data-user-slot]");
  const token = getAccessToken();
  const payload = decodeJwtPayload(token);
  if (slot && payload) {
    const badge = payload.job_title ? `<span class="pill pill-ghost">${payload.job_title}</span>` : "";
    slot.innerHTML = `<span class="muted">Logged in as</span> ${payload.username || "user"} ${badge}`;
  }
}
