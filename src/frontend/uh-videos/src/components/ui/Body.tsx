'use client'

import SearchIcon from '@mui/icons-material/Search';

import { Card } from "./Card";

export default function Body() {

  const videos = [
    {
      id: 1,
      name: "Clash Royale",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo0.png",
    },
    {
      id: 2,
      name: "Dota 2",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo1.png",
    },
    {
      id: 3,
      name: "FC 24",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo2.png",
    },
    {
      id: 1,
      name: "Clash Royale",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo0.png",
    },
    {
      id: 2,
      name: "Dota 2",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo1.png",
    },
    {
      id: 3,
      name: "FC 24",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo2.png",
    },
    {
      id: 1,
      name: "Clash Royale",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo0.png",
    },
    {
      id: 2,
      name: "Dota 2",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo1.png",
    },
    {
      id: 3,
      name: "FC 24",
      clasification: "Film",
      year: "2023",
      gender: "Adventure",
      language: "English",
      country: "USA",
      audience: "Kids",
      image: "/torneo2.png",
    },
  ];

  return (
    <div className="container  text-white">

      <div className="flex items-center my-[3%] max-w-lg mx-auto bg-white rounded-lg border border-gray-300 focus-within:ring-2 focus-within:ring-pink-500" style={{ backgroundColor: 'rgba(255, 255, 255, 0.9)' }}>
        <input
          type="text"
          placeholder="Busque su video..."
          className="flex-grow p-3 bg-transparent text-black rounded-l-lg focus:outline-none"
        />
        <button type="button" className="p-3">
          <SearchIcon style={{ color: '#333', fontSize: '1.5rem' }} />
        </button>
      </div>

      <div className="w-11/12 bg-[#ffffff45] rounded-lg mx-auto py-4 shadow-lg">
        {videos.map((video, x) => (
          <div
            key={x}
            className="ml-[2%] my-[2%] "
          >
            <Card video={video} />
          </div>
        ))}
      </div>

    </div >
  );
}
