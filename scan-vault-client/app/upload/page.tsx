"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Loader2, AlertCircle } from 'lucide-react'
import { SensitiveInfoSummary } from '@/components/sensitive-info-summary'
import { useToast } from "@/hooks/use-toast"
import { BackendService } from '@/services/backend-service'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [scanResult, setScanResult] = useState<any | null>(null)
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
      return
    }

    setIsLoading(true)
    setError(null)
    setScanResult(null)

    try {
      const result = await BackendService.scanFile(file)
     
      setScanResult(result)
      toast({
        title: "Success",
        description: "File scanned successfully!",
      })
    } catch (err) {
      console.error('Scan Error:', err)
      setError(err instanceof Error ? err.message : "An error occurred while scanning your file.")
    } finally {
      setIsLoading(false)
    }
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
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <Label htmlFor="file">File</Label>
                <Input 
                  id="file" 
                  type="file" 
                  onChange={handleFileChange} 
                  accept=".txt,.pdf,.docx,.csv,.jpg,.jpeg,.png" 
                  className="cursor-pointer"
                />
              </div>
              <p className="text-sm text-muted-foreground">
                Supported formats: .txt, .pdf, .docx, .csv, .jpg, .jpeg, .png (Max size: 10MB)
              </p>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button asChild variant="ghost">
              <Link href="/">Cancel</Link>
            </Button>
            <Button type="submit" disabled={isLoading}>
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
          <AlertDescription>An Error Occurred While Scanning Your File</AlertDescription>
          <div className="mt-4">
            <p className="text-sm text-muted-foreground">Possible reasons:</p>
            <ul className="list-disc list-inside text-sm text-muted-foreground">
              <li>File is too large</li>
              <li>File is not supported</li>
              <li>File is corrupted or password protected</li>
            </ul>
          </div>
        </Alert>
      )}

      {scanResult?.results && <SensitiveInfoSummary results={scanResult.results} />}
    </div>
  )
}

