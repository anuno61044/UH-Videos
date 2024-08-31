import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Movie.css'

export const Movie = ({ title, director, genres, date, description }) => {

    return (
        <div className='movie card shadow mb-4'>
            <h3>{title}</h3>
            <div className='d-flex'>
                <p className='tag'>Director:</p>
                <p className='info'>{director}</p>
            </div>
            <div className='d-flex'>
                <p className='tag'>Géneros:</p>
                <p className='info'>{genres}</p>
            </div>
            <div className='d-flex'>
                <p className='tag'>Fecha de lanzamiento:</p>
                <p className='info'>{date}</p>
            </div>
            <div className='d-flex'>
                <p className='tag'>Descripción:</p>
                <p className='info'>{description}</p>
            </div>
        </div>
    )
}

export default Movie;