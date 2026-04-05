async function loadRecipes() {
  const res = await fetch('/api/recipes');
  const data = await res.json();

  const grid = document.getElementById('recipe-grid');
  grid.innerHTML = "";

  data.forEach(r => {
    const div = document.createElement('div');
    div.className = "card";

    div.innerHTML = `
      <a href="${r.link}" target="_blank">
        <img src="${r.image}">
      </a>

      <h3>${r.title}</h3>

      <a class="file-link" href="/recipes/${r.file}" target="_blank">
        Open File
      </a>
    `;

    grid.appendChild(div);
  });
}

async function addRecipe() {
  const data = {
    title: document.getElementById("title").value,
    image: document.getElementById("image").value,
    link: document.getElementById("link").value,
    file: document.getElementById("file").value
  };

  await fetch('/api/add', {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  loadRecipes();
}

loadRecipes();
  loadRecipes();
}

loadRecipes();
