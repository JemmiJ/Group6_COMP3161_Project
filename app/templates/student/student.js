// Check if user is authenticated and is a student
function checkAuth(role) {
    const token = localStorage.getItem("token");
    const userRole = localStorage.getItem("role");
  
    if (!token || userRole !== role) {
      alert("Unauthorized. Redirecting to login.");
      window.location.href = "../index.html";
    }
  }
  
  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    window.location.href = "../index.html";
  }
  
  // Load student’s available courses
  function loadStudentCourses() {
    checkAuth("Student");
    fetch("http://localhost:8000/student/courses", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    })
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById("course-list");
        list.innerHTML = "";
        data.forEach(course => {
          list.innerHTML += `
            <div class="card mb-2">
              <div class="card-body">
                <h5>${course.CName}</h5>
                <p>${course.CCode}</p>
                <button onclick="enroll(${course.CID})" class="btn btn-primary">Enroll</button>
              </div>
            </div>`;
        });
      });
  }
  
  function enroll(cid) {
    fetch("http://localhost:8000/enroll", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({ course_id: cid })
    })
      .then(res => res.json())
      .then(msg => alert("Enrolled successfully!"));
  }
  
  // Load assignments
  function loadStudentAssignments() {
    checkAuth("Student");
    fetch("http://localhost:8000/student/assignments", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    })
      .then(res => res.json())
      .then(data => {
        const list = document.getElementById("assignment-list");
        list.innerHTML = "";
        data.forEach(a => {
          list.innerHTML += `
            <div class="card mb-2">
              <div class="card-body">
                <h5>${a.Title}</h5>
                <p>${a.Description}</p>
                <form onsubmit="submitAssignment(event, ${a.AssignId})">
                  <textarea class="form-control mb-2" name="content" placeholder="Submit work..." required></textarea>
                  <button class="btn btn-success">Submit</button>
                </form>
              </div>
            </div>`;
        });
      });
  }
  
  function submitAssignment(event, aid) {
    event.preventDefault();
    const content = event.target.elements["content"].value;
  
    fetch("http://localhost:8000/submit_assignment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("token")
      },
      body: JSON.stringify({ assignment_id: aid, submission_text: content })
    })
      .then(res => res.json())
      .then(msg => alert("Submitted successfully!"));
  }
  
  // Load forum threads
  function loadStudentForum() {
    checkAuth("Student");
    fetch("http://localhost:8000/forum_threads", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }
    })
      .then(res => res.json())
      .then(data => {
        const forum = document.getElementById("forum-threads");
        forum.innerHTML = "";
        data.forEach(thread => {
          forum.innerHTML += `
            <div class="card mb-2">
              <div class="card-body">
                <h5>${thread.Title}</h5>
                <p>${thread.Content}</p>
              </div>
            </div>`;
        });
      });
  
    document.getElementById("new-thread-form").onsubmit = (e) => {
      e.preventDefault();
      const title = document.getElementById("thread-title").value;
      const content = document.getElementById("thread-content").value;
  
      fetch("http://localhost:8000/forum_post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({ forum_id: 1, title, content }) // You may want to make forum_id dynamic
      }).then(() => {
        alert("Thread posted!");
        loadStudentForum();
      });
    };
  }
  