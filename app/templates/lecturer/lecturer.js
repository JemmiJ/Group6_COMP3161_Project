function checkAuth(role) {
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
  
  // Load Lecturer Assignments
  function loadLecturerAssignments() {
    checkAuth("Lecturer");
  
    fetch("http://localhost:8000/lecturer/assignments", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    })
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("assignment-list");
        container.innerHTML = "";
        data.forEach(a => {
          container.innerHTML += `
            <div class="card mb-2">
              <div class="card-body">
                <h5>${a.Title}</h5>
                <p>${a.Description}</p>
                <p><strong>Due:</strong> ${a.DueDate}</p>
              </div>
            </div>`;
        });
      });
  }
  
  // Upload Course Content
  function loadLecturerContent() {
    checkAuth("Lecturer");
  
    fetch("http://localhost:8000/lecturer/courses", {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
      .then(res => res.json())
      .then(data => {
        const select = document.getElementById("course-id");
        data.forEach(c => {
          select.innerHTML += `<option value="${c.CID}">${c.CName}</option>`;
        });
      });
  
    document.getElementById("upload-form").onsubmit = function (e) {
      e.preventDefault();
      const payload = {
        course_id: document.getElementById("course-id").value,
        section: document.getElementById("section").value,
        content: document.getElementById("content").value,
        content_type: document.getElementById("content-type").value
      };
  
      fetch("http://localhost:8000/upload_content", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(payload)
      }).then(() => {
        alert("Content uploaded!");
        document.getElementById("upload-form").reset();
      });
    };
  }
  
  // Forum management
  function loadLecturerForums() {
    checkAuth("Lecturer");
  
    fetch("http://localhost:8000/lecturer/courses", {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
      .then(res => res.json())
      .then(data => {
        const select = document.getElementById("forum-course");
        data.forEach(c => {
          select.innerHTML += `<option value="${c.CID}">${c.CName}</option>`;
        });
      });
  
    document.getElementById("new-forum-form").onsubmit = function (e) {
      e.preventDefault();
      const payload = {
        forum_name: document.getElementById("forum-name").value,
        course_id: document.getElementById("forum-course").value
      };
  
      fetch("http://localhost:8000/create_forum", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(payload)
      }).then(() => {
        alert("Forum created!");
        document.getElementById("new-forum-form").reset();
      });
    };
  }