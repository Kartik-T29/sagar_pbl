
// Global state for movies
let allMovies = [];
let filteredMovies = [];

// --- API Communication ---
const API_URL = 'http://127.0.0.1:5001/api';

async function fetchMovies() {
    try {
        const response = await fetch(`${API_URL}/movies`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allMovies = await response.json();
        filteredMovies = [...allMovies];
        loadMovies();
    } catch (error) {
        console.error("Failed to fetch movies:", error);
        document.getElementById('moviesGrid').innerHTML = '<p class="error-message">Could not load movies. Is the backend server running?</p>';
    }
}

async function searchMoviesAPI(query) {
    const moviesGrid = document.getElementById('moviesGrid');
    moviesGrid.innerHTML = '<p class="loading-message">Searching...</p>'; // Show loading message

    if (!query) {
        filteredMovies = [...allMovies];
        loadMovies();
        return;
    }
    try {
        const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        filteredMovies = await response.json();
        loadMovies();
    } catch (error) {
        console.error("Failed to search movies:", error);
        moviesGrid.innerHTML = '<p class="error-message">Search failed. Please try again later.</p>';
    }
}

async function predictMovieSuccessAPI(movieData) {
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movieData)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const prediction = await response.json();
        displayPredictionResults(movieData.title, prediction);
    } catch (error) {
        console.error("Failed to get prediction:", error);
        alert("Prediction service is currently unavailable.");
    }
}


// --- UI Rendering ---

function loadMovies() {
    const moviesGrid = document.getElementById('moviesGrid');
    moviesGrid.innerHTML = '';

    if (filteredMovies.length === 0) {
        moviesGrid.innerHTML = '<p class="no-movies">No movies found. Try a different search term.</p>';
        return;
    }

    filteredMovies.forEach(movie => {
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.onclick = () => showMovieDetails(movie);

        // Use the pre-processed genre_names from the backend
        const genres = movie.genre_names || 'N/A';
        const rating = movie.vote_average ? movie.vote_average.toFixed(1) : 'N/A';

        card.innerHTML = `
            <img src="${movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 'https://via.placeholder.com/300x450/4A90E2/ffffff?text=No+Image'}" 
                 alt="${movie.title}" class="movie-poster">
            <div class="movie-info">
                <h3>${movie.title}</h3>
                <div class="movie-meta">
                    <span class="movie-genre">${genres}</span>
                    <span class="movie-rating">⭐ ${rating}</span>
                </div>
            </div>
        `;

        moviesGrid.appendChild(card);
    });
}

function showMovieDetails(movie) {
    const modal = document.getElementById('movieModal');
    const modalBody = document.getElementById('modalBody');

    const genres = movie.genre_names || 'N/A';
    const rating = movie.vote_average ? movie.vote_average.toFixed(1) : 'N/A';
    const releaseDate = movie.release_date ? new Date(movie.release_date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) : 'N/A';

    modalBody.innerHTML = `
        <img src="${movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 'https://via.placeholder.com/200x300/4A90E2/ffffff?text=No+Image'}" 
             alt="${movie.title}" class="modal-poster">
        <div class="modal-details">
            <h2>${movie.title}</h2>
            <p><strong>Genre:</strong> ${genres}</p>
            <p><strong>Release Date:</strong> ${releaseDate}</p>
            <p><strong>Rating:</strong> ⭐ ${rating} / 10</p>
            <p><strong>Overview:</strong> ${movie.overview || 'No overview available.'}</p>
        </div>
    `;

    modal.style.display = 'block';
}

// --- (Prediction form functions remain the same) ---
function displayPredictionResults(title, prediction) {
    const resultDiv = document.getElementById('predictionResult');
    resultTitle.textContent = title;
    resultRevenue.textContent = `₹${prediction.revenue} Cr`;
    resultScore.textContent = `${prediction.score}%`;
    resultROI.textContent = `${prediction.roi}x`;
    // ... (rest of the function is unchanged)
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// --- Event Listeners ---

document.addEventListener('DOMContentLoaded', function() {
    fetchMovies();
    document.getElementById('upcoming').style.display = 'none'; // Hide upcoming section
});

document.getElementById('movieSearch').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchMoviesAPI(this.value);
    }
});

document.querySelector('.search-box button').addEventListener('click', () => {
    const searchTerm = document.getElementById('movieSearch').value;
    searchMoviesAPI(searchTerm);
});

document.getElementById('predictForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const movieData = {
        title: document.getElementById('title').value,
        budget: parseFloat(document.getElementById('budget').value),
        // Add other form fields as needed
    };
    predictMovieSuccessAPI(movieData);
});

function closeModal() {
    document.getElementById('movieModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('movieModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Dummy functions for elements that might be in HTML but are not used
function generateSuccessFactors(prediction) { return []; }