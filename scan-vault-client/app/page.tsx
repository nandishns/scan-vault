import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowUpCircle, FileSearch, Lock, BarChart, Upload, FileText } from 'lucide-react'
import { GridBackground } from "@/components/grid-background"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-black text-white">
      <header className="relative py-24 md:py-32 overflow-hidden">
        <GridBackground />
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10 lg:mt-20">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-6 animate-fade-in">ScanVault</h1>
            <p className="text-xl sm:text-2xl mb-8 animate-fade-in animation-delay-200">
              The AI-Powered Sensitive Data Detection Platform
            </p>
            <p className="text-lg mb-8 animate-fade-in animation-delay-400">
              ScanVault is software aiming to revolutionize data protection. We&apos;re leveraging the power of AI to create
              <span className="font-bold"> cutting-edge sensitive data detection</span>
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4 animate-fade-in animation-delay-600">
              <Button asChild size="lg" variant="default" className="bg-white text-black hover:bg-gray-200 transition-colors">
                <Link href="/upload">Scan Now!</Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="bg-transparent text-white border-white hover:bg-white hover:text-black transition-colors">
                <Link href="/docs">Docs</Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow">
        <section className="py-24 bg-white text-black">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16">Why Choose ScanVault?</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[
                { title: "AI-Driven Detection", description: "Advanced algorithms identify sensitive data like PII, PHI, and PCI with high accuracy.", icon: <FileSearch className="h-12 w-12 mb-4 text-blue-500" /> },
                { title: "Secure Processing", description: "Your files are processed securely and classified without permanent storage.", icon: <Lock className="h-12 w-12 mb-4 text-green-500" /> },
                { title: "Comprehensive Insights", description: "Retrieve scan results with detailed classifications and data breakdowns.", icon: <BarChart className="h-12 w-12 mb-4 text-purple-500" /> },
                { title: "Easy Management", description: "Upload, retrieve, and delete scan records from a simple, intuitive interface.", icon: <FileText className="h-12 w-12 mb-4 text-orange-500" /> },
              ].map((feature, index) => (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow bg-gray-100 text-black">
                  <CardHeader>
                    <CardTitle className="flex flex-col items-center">
                      {feature.icon}
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p>{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="py-24 bg-black text-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16">How ScanVault Works</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {[
                { title: "Upload Your File", description: "Choose any supported file format from your device.", icon: <Upload className="h-12 w-12 mb-4 text-blue-500" /> },
                { title: "AI Analysis", description: "Our system analyzes your file using advanced machine learning techniques.", icon: <FileSearch className="h-12 w-12 mb-4 text-purple-500" /> },
                { title: "Access Results", description: "Retrieve detailed scan results and manage your data effortlessly.", icon: <ArrowUpCircle className="h-12 w-12 mb-4 text-green-500" /> },
              ].map((step, index) => (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow bg-gray-900">
                  <CardHeader>
                    <CardTitle className="flex flex-col items-center">
                      {step.icon}
                      {step.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p>{step.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="py-24 bg-white text-black">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl sm:text-4xl font-bold mb-8">Start Scanning Your Files Now!</h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              ScanVault helps you detect sensitive data in seconds.
              Upload your files securely, and let our AI handle the rest.
            </p>
            <Button asChild size="lg" className="bg-black text-white hover:bg-gray-800 transition-colors">
              <Link href="/upload">Upload File</Link>
            </Button>
          </div>
        </section>
      </main>
    </div>
  )
}

