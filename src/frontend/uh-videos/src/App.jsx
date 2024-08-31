import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import React, { useState, useEffect } from 'react';
import Movie from './components/MovieInfo/Movie';

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
      <div className="relative">
        <div className="d-flex justify-content-center">
          <img className="w-50" src="../../../public/VisualesTube.jpg" alt=""/>
        </div>
        <div className="user-admin">
          <button className="btn">Login</button>
          <button className="btn btn-primary">Registrarse</button>
        </div>
        <nav className="navbar navbar-expand-lg">            
              <div className="container-fluid">
                  <a className="navbar-brand text-light" href="/">Movies</a>
                  <form className="d-flex w-100" role="search">
                      <input className="form-control me-5 ms-5" type="search" placeholder="Search" aria-label="Search"/>
                      <button className="btn btn-outline-light text-light" type="submit">Search</button>
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
                key={index}
              />
            ))
        )}
        </div>
      </div>
  );
}

export default App;