// frontend/script.js

document.addEventListener('DOMContentLoaded', function () {
  const startBtn = document.getElementById('startBtn');
  if (startBtn) {
    startBtn.addEventListener('click', function () {
      alert('SkillSnacks AI Bot is launching…');
    });
  }

  // Fetch and render all skills on page load
  fetchSkills();
});

// Fetch all skills and render them
async function fetchSkills() {
  try {
    const response = await fetch('/api/skills');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const skills = await response.json();
    renderSkills(skills);
  } catch (error) {
    console.error("Error fetching skills:", error);
    const errorMsg = document.getElementById('error-message');
    if (errorMsg) {
      errorMsg.innerText = "Failed to load skills. Please try again later.";
    }
  }
}

// Render skill cards
function renderSkills(skills) {
  const container = document.getElementById('skills-container');
  if (!container) return;
  container.innerHTML = '';
  skills.forEach(skill => {
    const card = document.createElement('div');
    card.className = 'skill-card';
    card.innerHTML = `<h3>${skill.title}</h3><p>${skill.description}</p>
      <button onclick="loadSkill('${skill.id}')">Learn ${skill.title}</button>`;
    container.appendChild(card);
  });
}

// Load a single skill's details
async function loadSkill(skill) {
  const container = document.getElementById("skill-container");
  if (!container) return;
  container.innerHTML = "Loading...";

  try {
    const res = await fetch(`/api/skills/${skill}`);
    const data = await res.json();

    if (data.error) {
      container.innerHTML = `<p style="color:red">${data.error}</p>`;
      return;
    }

    container.innerHTML = `
      <h2>${data.title}</h2>
      <p><strong>Category:</strong> ${data.category}</p>
      <p>${data.introduction}</p>
      <h4>Materials</h4>
      <ul>${data.materials.map(m => `<li>${m}</li>`).join('')}</ul>
      <h4>Steps</h4>
      <ol>${data.steps.map(s => `<li>${s}</li>`).join('')}</ol>
      <h4>Tips</h4>
      <p>${data.tips}</p>
      <h4>Assessment</h4>
      <p>${data.assessment}</p>
    `;
  } catch (err) {
    container.innerHTML = "<p style='color:red'>Failed to load skill data.</p>";
  }
}


