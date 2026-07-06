// =====================================================================
// CropCareAI — Lamp Login Experience
// =====================================================================

import { loginWithGoogle } from "./auth.js";
import { checkUserSession } from "./session.js";

(() => {
  const app = document.getElementById("app");

  const lampBtn = document.getElementById("lampBtn");

  const lampSvg = document.getElementById("lampSvg");

  const toggleChevron = document.getElementById("toggleChevron");

  const mobileClose = document.getElementById("mobileClose");

  const loginPanel = document.getElementById("loginPanel");

  const googleBtn = document.getElementById("googleBtn");

  let isOpen = false;

  let toastTimer = null;

  // =====================================================
  // Lamp Open / Close
  // =====================================================

  function setOpen(open) {
    isOpen = open;

    app.classList.toggle("is-open", open);

    lampBtn.classList.toggle("is-lit", open);

    lampSvg.classList.toggle("is-lit", open);

    lampBtn.setAttribute("aria-pressed", String(open));

    lampBtn.setAttribute(
      "aria-label",

      open ? "Turn off lamp" : "Turn on lamp",
    );

    loginPanel.setAttribute(
      "aria-hidden",

      String(!open),
    );
  }

  function toggleLamp() {
    setOpen(!isOpen);
  }

  // =====================================================
  // Toast
  // =====================================================

  function showToast(message) {
    let toast = app.querySelector(".toast");

    if (!toast) {
      toast = document.createElement("div");

      toast.className = "toast";

      app.appendChild(toast);
    }

    toast.textContent = message;

    requestAnimationFrame(() => {
      toast.classList.add("show");
    });

    clearTimeout(toastTimer);

    toastTimer = setTimeout(() => {
      toast.classList.remove("show");
    }, 2500);
  }

  // =====================================================
  // Events
  // =====================================================

  lampBtn.addEventListener("click", toggleLamp);

  toggleChevron.addEventListener("click", toggleLamp);

  if (mobileClose) {
    mobileClose.addEventListener(
      "click",

      () => setOpen(false),
    );
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isOpen) {
      setOpen(false);
    }
  });

  // =====================================================
  // Google Login
  // =====================================================

  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      try {
        googleBtn.disabled = true;

        googleBtn.innerHTML = "Signing In...";

        const user = await loginWithGoogle();

        showToast(`Welcome ${user.name}!`);

        console.log(user);

        setTimeout(() => {
          window.location.href = "http://localhost:8501";
        }, 1200);
      } catch (error) {
        console.error(error);

        alert(error.message);

        showToast("Login Failed");
      } finally {
        googleBtn.disabled = false;

        googleBtn.innerHTML = "Continue with Google";
      }
    });
  }

  // =====================================================
  // Check Existing Session
  // =====================================================

  checkUserSession();

  // =====================================================
  // Initial State
  // =====================================================

  setOpen(false);
})();
