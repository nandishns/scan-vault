"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { Eye, Trash2 } from 'lucide-react'

// Update the mock data
const mockScannedFiles = [
  { 
    id: 1, 
    name: "document1.pdf", 
    uploadDate: "2024-03-15", 
    sensitiveInfo: [
      { category: "PII", type: "SSN", value: "123-45-6789" },
      { category: "Financial", type: "Credit Card", value: "**** **** **** 1234" }
    ]
  },
  { 
    id: 2, 
    name: "spreadsheet.csv", 
    uploadDate: "2024-03-14", 
    sensitiveInfo: [
      { category: "PII", type: "Email", value: "john.doe@example.com" },
      { category: "Financial", type: "PAN", value: "*****6789" }
    ]
  },
  { 
    id: 3, 
    name: "report.docx", 
    uploadDate: "2024-03-13", 
    sensitiveInfo: [
      { category: "PII", type: "Phone Number", value: "(555) 123-4567" }
    ]
  },
];

export default function ViewFilesPage() {
  const [scannedFiles, setScannedFiles] = useState(mockScannedFiles)
  const [selectedFile, setSelectedFile] = useState<typeof mockScannedFiles[0] | null>(null)
  const [isDetailsOpen, setIsDetailsOpen] = useState(false)

  const handleDelete = (id: number) => {
    setScannedFiles(scannedFiles.filter(file => file.id !== id))
  }

  const handleViewDetails = (file: typeof mockScannedFiles[0]) => {
    setSelectedFile(file)
    setIsDetailsOpen(true)
  }

  return (
    <div className="container mx-auto py-12 mt-20">
      <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center">View Scanned Files</h1>
      {scannedFiles.length > 0 ? (
        <Card className="max-w-6xl mx-auto">
          <CardHeader>
            <CardTitle>Scanned Files</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>File Name</TableHead>
                  <TableHead>Upload Date</TableHead>
                  <TableHead>Sensitive Info</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {scannedFiles.map((file) => (
                  <TableRow key={file.id}>
                    <TableCell>{file.name}</TableCell>
                    <TableCell>{file.uploadDate}</TableCell>
                    <TableCell>
                      <ul className="list-disc pl-4">
                        {file.sensitiveInfo.map((info, index) => (
                          <li key={index}>
                            <strong>{info.type}:</strong> {info.value}
                          </li>
                        ))}
                      </ul>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Button size="sm" variant="outline" onClick={() => handleViewDetails(file)} className="hover:bg-primary hover:text-primary-foreground transition-colors">
                          <Eye className="h-4 w-4 mr-1" /> View
                        </Button>
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button size="sm" variant="destructive" className="hover:bg-red-700 transition-colors">
                              <Trash2 className="h-4 w-4 mr-1" /> Delete
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                              <AlertDialogDescription>
                                This action cannot be undone. This will permanently delete the scan record for {file.name}.
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel className="hover:bg-muted transition-colors">Cancel</AlertDialogCancel>
                              <AlertDialogAction onClick={() => handleDelete(file.id)} className="hover:bg-red-700 transition-colors">Delete</AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      ) : (
        <Card className="text-center">
          <CardHeader>
            <CardTitle>No files scanned yet</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Upload a file to get started!</p>
          </CardContent>
          <CardFooter className="justify-center">
            <Button asChild className="hover:bg-blue-600 transition-colors">
              <Link href="/upload">Upload File</Link>
            </Button>
          </CardFooter>
        </Card>
      )}

      <Dialog open={isDetailsOpen} onOpenChange={setIsDetailsOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Scan Details</DialogTitle>
          </DialogHeader>
          {selectedFile && (
            <>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">
                    File Name
                  </Label>
                  <Input id="name" value={selectedFile.name} className="col-span-3" readOnly />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="uploadDate" className="text-right">
                    Upload Date
                  </Label>
                  <Input id="uploadDate" value={selectedFile.uploadDate} className="col-span-3" readOnly />
                </div>
                <div className="grid grid-cols-4 items-start gap-4">
                  <Label htmlFor="sensitiveInfo" className="text-right">
                    Sensitive Info
                  </Label>
                  <div className="col-span-3">
                    <ul className="list-disc pl-4">
                      {selectedFile.sensitiveInfo.map((info, index) => (
                        <li key={index}>
                          <strong>{info.type}:</strong> {info.value}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
              <DialogFooter>
                <Button onClick={() => setIsDetailsOpen(false)} className="hover:bg-blue-600 transition-colors">Close</Button>
              </DialogFooter>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

