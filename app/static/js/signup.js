document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  form.addEventListener("submit", (e) => {
    const userId = form.querySelector('input[name="user_id"]').value.trim();
    const password = form.querySelector('input[name="password"]').value.trim();
    const firstName = form.querySelector('input[name="first_name"]').value.trim();
    const lastName = form.querySelector('input[name="last_name"]').value.trim();

    if (!userId || !password || !firstName || !lastName) {
      e.preventDefault();
      alert("Please fill in all the required fields.");
    }
  });
});