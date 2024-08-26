import { FC, useState } from 'react';
import Image from "next/image";
import { Rating } from '@mui/material';
import video from '@/types/video';

interface Movie {
    id: number;
    title: string;
    genre: string;
    director: string;
    description: string;
    release_date: string;
    // image: string; // Agrega una imagen a tu modelo si aún no lo has hecho
    ratings: number[]; // Array de puntuaciones
}

interface prop {
    movie: Movie;
}

export const Card: FC<prop> = ({ movie }) => {
    const [userRating, setUserRating] = useState<number | null>(null);

    const handleRatingChange = (event: React.SyntheticEvent, newValue: number | null) => {
        setUserRating(newValue);

        // Enviar la nueva calificación a la API
        fetch(`http://localhost:8000/api/movies/${movie.id}/rate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: 1, // Cambia por el ID del usuario autenticado
                movie_id: movie.id,
                score: newValue,
            }),
        })
            .then(response => response.json())
            .then(data => console.log('Rating submitted:', data))
            .catch(error => console.error('Error submitting rating:', error));
    };

    const averageRating = movie.ratings.length > 0 ? movie.ratings.reduce((a, b) => a + b) / movie.ratings.length : 0;

    return (
        <div className="flex">
            {/* <div className='w-1/2'>
                <Image
                    src={movie.image}
                    alt="Image"
                    fill
                    className="image"
                />
            </div> */}
            <div className='w-2/3 ml-[2%]'>
                <div className='text-4xl text-white font-bold'>{movie.title}</div>
                <div className='text-3xl text-gray-300 font-bold mt-[2%]'>{movie.genre}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>Director: {movie.director}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>Fecha de lanzamiento: {movie.release_date}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>{movie.description}</div>

                <div className='mt-[2%]'>
                    <Rating
                        name={`movie-rating-${movie.id}`}
                        value={userRating || averageRating}
                        precision={0.5}
                        onChange={handleRatingChange}
                    />
                    <div className='text-gray-400 mt-[1%]'>Calificación promedio: {averageRating.toFixed(1)}</div>
                </div>
            </div>
        </div>
    );
}
