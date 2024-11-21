import Link from "next/link"
import { Button } from "@/components/ui/button"
import { MobileSidebar } from './mobile-sidebar'

export function Navbar() {
  return (
    <nav className="bg-black/90 text-white fixed top-0 left-0 right-0 z-50 border-b border-gray-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link href="/" className="flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-white">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" />
              <path d="M8 11h8" />
              <path d="M12 15V7" />
            </svg>
            <span className="font-bold text-xl text-white">ScanVault</span>
          </Link>
          <div className="flex items-center space-x-6">
            <div className="hidden md:flex items-center space-x-6">
              <Link href="/upload" className="text-gray-300 hover:text-white transition-colors">
                Upload
              </Link>
              <Link href="/view-files" className="text-gray-300 hover:text-white transition-colors">
                View Files
              </Link>
              <Button asChild variant="default" size="sm" className="bg-white text-black hover:bg-gray-200 transition-colors">
                <Link href="/upload">Get Started</Link>
              </Button>
            </div>
            <MobileSidebar />
          </div>
        </div>
      </div>
    </nav>
  )
}

