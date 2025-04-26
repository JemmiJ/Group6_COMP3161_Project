function checkAuth(role = "Admin") {
    const token = localStorage.getItem("token");
    const userRole = localStorage.getItem("role");
    if (!token || userRole !== role) {
      alert("Unauthorized. Redirecting to login.");
      window.location.href = "../index.html";
    }
  }
  
  function logout() {
    localStorage.clear();
    window.location.href = "../index.html";
  }
  
  // 📊 Dashboard Stats
  function loadAdminStats() {
    checkAuth("Admin");
  
    fetch("http://localhost:8000/admin/stats", {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
      .then(res => res.json())
      .then(data => {
        const statsDiv = document.getElementById("stats");
        statsDiv.innerHTML = `
          <div class="col-md-4"><div class="alert alert-primary">Students: ${data.students}</div></div>
          <div class="col-md-4"><div class="alert alert-success">Lecturers: ${data.lecturers}</div></div>
          <div class="col-md-4"><div class="alert alert-warning">Courses: ${data.courses}</div></div>
        `;
      });
  }
  
  // 📚 Load lecturers for course creation
  function loadLecturersForCourseForm() {
    checkAuth("Admin");
  
    fetch("http://localhost:8000/admin/lecturers", {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
      .then(res => res.json())
      .then(data => {
        const select = document.getElementById("lecID");
        data.forEach(lec => {
          select.innerHTML += `<option value="${lec.LecID}">${lec.LFirstName} ${lec.LLastName}</option>`;
        });
      });
  
    document.getElementById("courseForm").onsubmit = function (e) {
      e.preventDefault();
      const course = {
        course_name: document.getElementById("courseName").value,
        course_code: document.getElementById("courseCode").value,
        department: document.getElementById("department").value,
        lec_id: document.getElementById("lecID").value
      };
  
      fetch("http://localhost:8000/create_course", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(course)
      })
        .then(res => res.json())
        .then(msg => {
          alert("Course created!");
          document.getElementById("courseForm").reset();
        });
    };
  }
  
  // 👥 Load all users
  function loadAllUsers() {
    checkAuth("Admin");
  
    fetch("http://localhost:8000/admin/users", {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
      .then(res => res.json())
      .then(data => {
        const userList = document.getElementById("user-list");
        userList.innerHTML = "";
        data.forEach(user => {
          userList.innerHTML += `
            <div class="card mb-2">
              <div class="card-body">
                <strong>${user.role}</strong>: ${user.name} (${user.id})
              </div>
            </div>`;
        });
      });
  }
  