import Link from 'next/link';
import { GithubButton } from '@/components/ui/github-button'; // Importing your new component
import { IconLeaf } from '@tabler/icons-react';

export default function Header() {
  return (
    <header className="absolute top-0 left-0 z-20 w-full p-4 md:p-6">
      <nav className="flex w-full items-center justify-between">

        {/* Left Side -- Name of Project  */}
        <Link
          href="/"
          className="flex items-center gap-2 px-4 py-2 rounded-full bg-black border border-gray-700 text-white transition-all hover:bg-neutral-900 hover:border-gray-500 hover:scale-105"
        >
          <IconLeaf className="w-5 h-5 text-green-400" />
          <span className="text-lg font-bold tracking-wider">Fluora Care</span>
        </Link>

        {/* Right Side --  Github link */}
        <GithubButton
          // see https://reui.io/docs/github-button for more variables
          initialStars={1}
          label=""
          targetStars={5}

          repoUrl="https://github.com/Qar-Raz/mlops_project.git"

          filled = {true}
          animationDuration= {5}
          roundStars={true}
          // below line can be commented out for clear black button --@Qamar
          className="bg-gray-900/50 border-gray-700 text-gray-200 hover:bg-gray-800/50 hover:border-gray-600"
        />

      </nav>
    </header>
  );
}
