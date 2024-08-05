import { AppBar, Toolbar } from '@mui/material';
import Link from 'next/link'
import Image from 'next/image';

export const Footer = () => {
    return (
        <div>

            <AppBar position='sticky' elevation={0} className='bg-[#4f4577] py-[0.5%]'>
                <Toolbar>

                    <div className='w-1/12 text-xs'>Power by:</div>
                    <div className='w-[4%] -ml-[3%]'>
                        <Link href={"/"}>
                            <Image src="/matcom.png" className="image mt-[5%] " alt="MatCom" fill />
                        </Link>
                    </div>

                    <div className='mx-auto text-xs'>© uh-videos. Todos los derechos reservados. 2024</div>
                </Toolbar>
            </AppBar>
        </div >
    )
}