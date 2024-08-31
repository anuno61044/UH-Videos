import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Tooltip, OverlayTrigger } from 'react-bootstrap';
import './Movie.css';

export const Movie = ({ title, director, genres, date, description, explanation }) => {
    return (
        <OverlayTrigger
            placement="top"
            delay={{ show: 2000, hide: 100 }} // Muestra el tooltip después de 2 segundos
            overlay={
                <Tooltip id={`tooltip-${title}`}>
                    {explanation}
                </Tooltip>
            }
        >
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
        </OverlayTrigger>
    );
};

export default Movie;
