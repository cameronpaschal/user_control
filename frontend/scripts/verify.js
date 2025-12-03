import { fetchJson, setStatus, setNavUser, wireLogoutButtons } from "./api.js";

setNavUser();
wireLogoutButtons();

const form = document.querySelector("#verify-form");
const statusBox = document.querySelector("#verify-status");
const params = new URLSearchParams(window.location.search);

async function verifyToken(token) {
  if (!token) {
    setStatus(statusBox, "Missing token", "error");
    return;
  }
  setStatus(statusBox, "Verifying token…", "info");
  try {
    const res = await fetchJson(`/auth/email-verify?token=${encodeURIComponent(token)}`);
    setStatus(statusBox, res?.status || "Email verified!", "success");
  } catch (err) {
    setStatus(statusBox, err.message || "Verification failed", "error");
  }
}

form?.addEventListener("submit", (event) => {
  event.preventDefault();
  const token = new FormData(form).get("token")?.toString().trim();
  verifyToken(token);
});

const tokenFromUrl = params.get("token");
if (tokenFromUrl) {
  const tokenInput = form?.elements.namedItem("token");
  if (tokenInput && "value" in tokenInput) {
    tokenInput.value = tokenFromUrl;
  }
  verifyToken(tokenFromUrl);
}
