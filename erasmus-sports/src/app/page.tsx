import Image from "next/image";
import Link from "next/link";
import PlayerCard from './components/PlayerCard/PlayerCard'

export default function Home() {
  return (
    <main>
      <h1>Hello World.</h1>
      <Link href='/analyzer'>Analyzer</Link>
      <PlayerCard />
    </main>
  );
}
