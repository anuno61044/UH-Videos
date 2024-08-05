import { FC } from 'react';
import Image from "next/image"
import video from '@/types/video';

interface prop {
    video: video
    // onDelete: (id: string) => Promise<void>
}

export const Card: FC<prop> = ({ video }) => {
    return (
        <div className="flex">

            <div className='w-1/2'>
                <Image
                    src={video.image}
                    alt="Image"
                    fill
                    className="image"
                />
            </div>
            <div className='w-2/3 ml-[2%]'>
                <div className='text-4xl text-white font-bold'>{video.name}</div>
                <div className='text-3xl text-gray-300 font-bold mt-[2%]'>{video.clasification}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>{video.year}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>{video.gender}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>{video.audience}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>{video.language}</div>
                <div className='text-1xl text-gray-300 mt-[1%]'>{video.country}</div>
            </div>
        </div>
    )
}