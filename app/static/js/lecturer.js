document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const inputs = form.querySelectorAll("input, textarea");
      let empty = false;
      inputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value.trim()) {
          empty = true;
        }
      });
      if (empty) {
        e.preventDefault();
        alert("Please complete all required fields before submitting.");
      }
    });
  });
});
