"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Loader2, AlertCircle, CheckCircle2 } from 'lucide-react'
import { SensitiveInfoSummary } from '@/components/sensitive-info-summary'
import { useToast } from "@/hooks/use-toast"

interface SensitiveInfo {
  category: string;
  type: string;
  value: string;
}

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [sensitiveInfo, setSensitiveInfo] = useState<SensitiveInfo[] | null>(null);
  const { toast } = useToast()

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError("Please select a file to upload.")
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please select a file to upload.",
      })
      return
    }

    setIsLoading(true)
    setError(null)
    setSuccess(false)
    setSensitiveInfo(null)

    // Simulating file upload and scanning
    await new Promise(resolve => setTimeout(resolve, 3000))

    // For demonstration purposes, we'll randomly succeed or fail
    if (Math.random() > 0.5) {
      setSuccess(true)
      setSensitiveInfo([
        { category: "Personally Identifiable Information (PII)", type: "Social Security Number", value: "123-45-6789" },
        { category: "Personally Identifiable Information (PII)", type: "Driver's License Number", value: "D1234567" },
        { category: "Financial Information", type: "Credit Card Number", value: "**** **** **** 1234" },
        { category: "Financial Information", type: "Bank Account Number", value: "*****6789" },
        { category: "Health Information", type: "Medical Record Number", value: "MRN12345" },
        { category: "Health Information", type: "Health Insurance ID", value: "HI987654321" }
      ]);
      toast({
        title: "Success",
        description: "File scanned successfully!",
      })
    } else {
      setError("An error occurred while scanning your file. Please try again.")
      toast({
        variant: "destructive",
        title: "Error",
        description: "An error occurred while scanning your file. Please try again.",
      })
    }

    setIsLoading(false)
  }

  return (
    <div className="container mx-auto py-12 mt-20">
      <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center">Upload File to Scan</h1>
      <Card className="max-w-md mx-auto">
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>Choose a file to scan</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid w-full items-center gap-4 cursor-pointer">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="file">File</Label>
                <Input id="file" type="file" onChange={handleFileChange} accept=".txt,.pdf,.docx,.csv" style={{cursor: 'pointer'}}/>
              </div>
              <p className="text-sm text-muted-foreground">
                Supported formats: .txt, .pdf, .docx, .csv (Max size: 10MB)
              </p>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button asChild variant="ghost" className="hover:bg-muted transition-colors">
              <Link href="/">Cancel</Link>
            </Button>
            <Button type="submit" disabled={isLoading} className="hover:bg-gray-200 transition-colors">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Scanning...
                </>
              ) : (
                "Scan File"
              )}
            </Button>
          </CardFooter>
        </form>
      </Card>

      {error && (
        <Alert variant="destructive" className="mt-4 max-w-md mx-auto">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="mt-4 max-w-md mx-auto">
          <CheckCircle2 className="h-4 w-4" />
          <AlertTitle>Success</AlertTitle>
          <AlertDescription>
            File scanned successfully! 
            <Link href="/view-files" className="underline ml-1 hover:text-primary transition-colors">
              View results in &apos;View Scanned Files&apos;.
            </Link>
          </AlertDescription>
        </Alert>
      )}

      {success && sensitiveInfo && (
        <SensitiveInfoSummary 
          sensitiveInfo={sensitiveInfo} 
          onSave={() => {
            // Here you would typically save the data to your backend
            console.log("Saving sensitive information summary")
          }} 
        />
      )}
    </div>
  )
}

