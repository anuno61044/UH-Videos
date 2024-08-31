import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import React, { useState, useEffect } from 'react';
import Movie from './components/MovieInfo/Movie';
import LoginModal from './components/LoginModal/LoginModal';
import RegisterMOdal from './components/RegisterModal/RegisterModal';

function App() {
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);


  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/movies/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const fetchedMovies = data.movies || data.results || data; // Ajusta según la estructura de tu API
        setMovies(fetchedMovies);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []); // El arreglo vacío significa que solo se ejecutará una vez al montaje del componente

  return (
    <>
      <div class="relative">
        <div class="d-flex justify-content-center">
          <img class="w-50" src="../../../public/VisualesTube.jpg" alt="" srcset="" />
        </div>
        <div class="user-admin">
          <div className='me-3'>
            <LoginModal/>
          </div>
          <RegisterMOdal/>
        </div>
        <nav class="navbar navbar-expand-lg">            
              <div class="container-fluid">
                  <a class="navbar-brand text-light" href="#">Movies</a>
                  <form class="d-flex w-100" role="search">
                      <input class="form-control me-5 ms-5" type="search" placeholder="Search" aria-label="Search"/>
                      <button class="btn btn-outline-light text-light" type="submit">Search</button>
                  </form>
              </div>
        </nav>

        <div className='movies-container'>
        {error ? (
            <div className="error-message">{error}</div>
          ) : (
            movies.map(movie => (
              <Movie 
                title={movie.title} 
                genres={movie.genre} 
                director={movie.director}
                date={movie.release_date}
                description={movie.description}
              />
            ))
        )}
        </div>
      </div>
    </>
  );
}

export default App;