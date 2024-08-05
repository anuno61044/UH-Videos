'use client'

import { Layout } from "@/components/layouts";
import Body from "@/components/ui/Body";
import Image from 'next/image';

export default function Home() {


  return (
    <Layout>
      <div className="container mx-auto text-white py-[0.5%]">
        <Body />
      </div>
    </Layout>
  );
}
