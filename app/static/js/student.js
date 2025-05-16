document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    const input = form.querySelector('input, textarea');
    if (!input || !input.value.trim()) {
      e.preventDefault();
      alert("Please fill in the form.");
    }
  });
});
