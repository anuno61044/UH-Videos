import { FC } from 'react'
import Head from "next/head"
import { Footer, Navbar } from '../ui';

interface Props {
    title?: string;
    children?: React.ReactNode;
}

export const Layout: FC<Props> = ({ title = 'uh-videos', children }) => {
    return (
        <div>
            <Head>
                <title>{title}</title>
            </Head>

            <Navbar />

            <div
                className="gradient">
                {children}
            </div>

            <Footer />
        </div>
    )
};