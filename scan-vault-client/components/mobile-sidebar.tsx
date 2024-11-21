import React from 'react'
import Link from 'next/link'
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Menu } from 'lucide-react'

export function MobileSidebar() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" className="md:hidden">
          <Menu className="h-6 w-6" />
          <span className="sr-only">Toggle menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-[300px] sm:w-[400px]">
        <nav className="flex flex-col gap-4">
          <Link href="/" className="text-lg font-semibold">
            Home
          </Link>
          <Link href="/upload" className="text-lg font-semibold">
            Upload
          </Link>
          <Link href="/view-files" className="text-lg font-semibold">
            View Files
          </Link>
          <Button asChild className="mt-4">
            <Link href="/upload">Get Started</Link>
          </Button>
        </nav>
      </SheetContent>
    </Sheet>
  )
}

