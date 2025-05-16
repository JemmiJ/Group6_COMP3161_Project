document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    const userId = form.querySelector('input[name="user_id"]').value.trim();
    const password = form.querySelector('input[name="password"]').value.trim();
    if (!userId || !password) {
      e.preventDefault();
      alert("Please enter both User ID and Password.");
    }
  });
});