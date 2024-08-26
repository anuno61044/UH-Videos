'use client'

import { useState, useEffect } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import { Card } from "./Card";

export default function Body() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    // Hacer la petición a la API de Django para obtener las películas
    fetch('http://localhost:8000/api/movies/')  // Ajusta la URL según sea necesario
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error('Error al obtener los datos:', error));
  }, []);

  return (
    <div className="container text-white">
      <div className="flex items-center my-[3%] max-w-lg mx-auto bg-white rounded-lg border border-gray-300 focus-within:ring-2 focus-within:ring-pink-500" style={{ backgroundColor: 'rgba(255, 255, 255, 0.9)' }}>
        <input
          type="text"
          placeholder="Busque su película..."
          className="flex-grow p-3 bg-transparent text-black rounded-l-lg focus:outline-none"
        />
        <button type="button" className="p-3">
          <SearchIcon style={{ color: '#333', fontSize: '1.5rem' }} />
        </button>
      </div>

      <div className="w-11/12 bg-[#ffffff45] rounded-lg mx-auto py-4 shadow-lg">
        {movies.map((movie, x) => (
          <div
            key={x}
            className="ml-[2%] my-[2%]"
          >
            <Card movie={movie} />
          </div>
        ))}
      </div>
    </div >
  );
}
