import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"

export function FAQ() {
  return (
    <section className="bg-black text-white py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl sm:text-4xl font-bold text-center mb-12">Frequently Asked Questions</h2>
        <Accordion type="single" collapsible className="w-full max-w-3xl mx-auto">
          <AccordionItem value="item-1">
            <AccordionTrigger>What types of files can I scan with ScanVault?</AccordionTrigger>
            <AccordionContent>
              ScanVault supports various file formats including .txt, .pdf, .docx, and .csv. We're constantly working on expanding our supported file types to accommodate more formats.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="item-2">
            <AccordionTrigger>How secure is my data when I upload it to ScanVault?</AccordionTrigger>
            <AccordionContent>
              We take data security very seriously. All uploads are encrypted in transit and at rest. We process files without permanent storage and delete them immediately after analysis. Our system adheres to strict privacy and security standards to ensure your sensitive information remains protected.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="item-3">
            <AccordionTrigger>What kind of sensitive information can ScanVault detect?</AccordionTrigger>
            <AccordionContent>
              ScanVault uses advanced AI algorithms to detect various types of sensitive information, including but not limited to Personally Identifiable Information (PII), Protected Health Information (PHI), and Payment Card Industry (PCI) data. This includes social security numbers, credit card numbers, medical record numbers, and more.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="item-4">
            <AccordionTrigger>How accurate is ScanVault's detection?</AccordionTrigger>
            <AccordionContent>
              ScanVault employs state-of-the-art machine learning models that are continuously trained and updated. While we strive for the highest accuracy, we recommend using ScanVault as a powerful tool in your overall data protection strategy, complemented by human review for critical documents.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
    </section>
  )
}

