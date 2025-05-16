document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    const courseCode = form.querySelector('input[name="course_code"]').value.trim();
    const courseName = form.querySelector('input[name="course_name"]').value.trim();
    const department = form.querySelector('input[name="department"]').value.trim();
    const lecturer = form.querySelector('input[name="lecturer"]').value.trim();

    if (!courseCode || !courseName || !department || !lecturer) {
      e.preventDefault();
      alert("Please fill in all course details.");
    }
  });
});
