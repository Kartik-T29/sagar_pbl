const API = "http://127.0.0.1:5001/api";

async function fetchMovies() {
    const res = await fetch(`${API}/movies`);
    const movies = await res.json();
    renderMovies(movies);
}

async function fetchUpcoming() {
    const res = await fetch(`${API}/upcoming`);
    const movies = await res.json();

    const grid = document.getElementById("upcomingGrid");
    grid.innerHTML = "";

    movies.forEach(m => {
        grid.innerHTML += `
        <div class="upcoming-card">
            <img class="upcoming-poster"
             src="https://image.tmdb.org/t/p/w500${m.poster_path}">
            <h3>${m.title}</h3>
            <p>📅 ${m.release_date?.split("T")[0]}</p>
        </div>`;
    });
}

async function searchMovies() {
    const q = document.getElementById("movieSearch").value;
    const res = await fetch(`${API}/search?q=${q}`);
    const movies = await res.json();
    renderMovies(movies);
}

function renderMovies(movies) {
    const grid = document.getElementById("moviesGrid");
    grid.innerHTML = "";

    movies.forEach(m => {
        grid.innerHTML += `
        <div class="movie-card">
            <img class="movie-poster"
             src="https://image.tmdb.org/t/p/w500${m.poster_path}">
            <h3>${m.title}</h3>
            <p>⭐ ${m.vote_average}</p>
            <p>${m.genre_names}</p>
        </div>`;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    fetchMovies();
    fetchUpcoming();
});
