import { AppBar, Toolbar } from '@mui/material';
import Link from 'next/link'
import Image from 'next/image';

export const Navbar = () => {
    return (
        <AppBar position='sticky' elevation={0} className='bg-[#4f4577]'>
            <Toolbar>
                <Link href={"/"} className=' flex'>
                    <div className='w-[15%]'>
                        <div className='m-auto'>
                            <Image src="/almamaterw.png" className="image " alt="UH" fill />
                        </div>
                    </div>
                    <div className='text-white my-auto pl-[5%]'>
                        uh-videos
                    </div>
                </Link>

                <div className='ml-auto'>
                    <Link href={"/profile"}>
                        <Image src="/pic.svg" className="image" alt="Profile" fill />
                    </Link>
                </div>
                <button className=' bg-transparent border text-white border-white rounded-lg py-[0.3%] px-[0.5%] ml-[1%]'>
                    CERRAR SESIÓN
                </button>
            </Toolbar>

        </AppBar>
    )
}