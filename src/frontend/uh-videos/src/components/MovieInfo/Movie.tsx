import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Tooltip, OverlayTrigger } from 'react-bootstrap';
import ReactStars from "react-rating-stars-component";
import './Movie.css';

export const Movie = ({ id, title, director, genre, date, url, description, explanation, onRate }) => {

    const handleRatingChange = (newRating) => {
        onRate(id, newRating);
    };

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
            <div>
                <div className='movie card shadow mb-4 position-relative'>
                    <div className="star-rating position-absolute top-0 end-0 m-2">
                        <ReactStars
                            count={5}
                            onChange={handleRatingChange}
                            size={24}
                            activeColor="#ffd700"
                        />
                    </div>
                    <a href={url} className='card-movie'>
                        <h3>{title}</h3>
                        <div className='d-flex'>
                            <p className='tag'>Director:</p>
                            <p className='info'>{director}</p>
                        </div>
                        <div className='d-flex'>
                            <p className='tag'>Género:</p>
                            <p className='info'>{genre}</p>
                        </div>
                        <div className='d-flex'>
                            <p className='tag'>Fecha de lanzamiento:</p>
                            <p className='info'>{date}</p>
                        </div>
                        <div className='d-flex'>
                            <p className='tag'>Descripción:</p>
                            <p className='info'>{description}</p>
                        </div>
                    </a>
                </div>
            </div>
        </OverlayTrigger>
    );
};

export default Movie;
